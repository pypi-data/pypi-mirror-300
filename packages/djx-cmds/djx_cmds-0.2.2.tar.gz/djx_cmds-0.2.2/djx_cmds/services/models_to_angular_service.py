import importlib
import inspect
import os
import pprint
from collections import defaultdict
from subprocess import check_output

import django
import inflection

from djx_cmds.format_with_jinja import format_with_jinja
from rest_framework import serializers


class ModelsToAngular:

    def __init__(self, file_path):
        self.file_path = file_path
        self.formly_type_map = {
            "TextField": "textarea",
            "BooleanField": "checkbox",
            "IntegerField": "input"
        }
        self.formly_props_type_map = {
            "DateField": "date",
            "IntegerField": "number",
            "FloatField": "number",
            "EmailField": "email",
        }

    def run(self):
        # self.check_client_folder()
        serializers_files = self.get_models_and_serializer_files()
        serializers_list = self.get_serializer_list(serializers_files)
        serializer_data = self.get_serializer_data(serializers_list)
        models_actions = self.get_models_and_actions(serializer_data)
        forms = self.generate_form_or_table(
            serializer_data, "FormlyFieldConfig", "formly.txt")
        tables = self.generate_form_or_table(serializer_data, "MtxGridColumn", "mtx_grid_table.txt")
        data = {**forms, **tables}
        self.configure_angular(models_actions)
        self.find_and_replace(self.file_path, data)

    def configure_angular(self, models_actions):
        all_command = [f'cd "{self.file_path}"']
        for element in models_actions:
            model_name = inflection.dasherize(models_actions[element]["model_name"]).lower()
            service_file_name = f"{model_name}.service.ts"
            if not self.check_if_file_exists(self.file_path, service_file_name):
                text = format_with_jinja(
                    models_actions[element],
                    "angular.txt"
                )
                all_command += text.split("\n")
        cmds = " && ".join(all_command)
        output = check_output(cmds, shell=True)
        print(output)

    @staticmethod
    def get_models_and_actions(serializer_data):
        action_data = defaultdict(list)
        for key in serializer_data:
            data = serializer_data[key]
            model_name = data['model_name']
            action = data["serializer_name"].replace(model_name, "").lower()
            action = action if action else "list"
            action_data[model_name].append(action)

        result = {serializer_data[key]["model_name"]: {
            "actions": action_data[serializer_data[key]["model_name"]],
            "model_name": serializer_data[key]["model_name"],
            "app_name": serializer_data[key]["app_name"]
        } for key in serializer_data}
        return result

    @staticmethod
    def check_if_file_exists(file_path, file_name):
        for root, dirs, files in os.walk(file_path):
            if file_name in files:
                return True
        return False

    @staticmethod
    def find_and_replace(file_path, data):
        for root, dirs, files in os.walk(file_path):
            for file_name in files:
                full_path = os.path.join(root, file_name)

                with open(full_path, 'r', encoding='utf-8') as file:
                    try:
                        file_content = file.read()
                    except UnicodeDecodeError:
                        continue

                modified_content = file_content
                for key, value in data.items():
                    modified_content = modified_content.replace(key, value)

                if modified_content != file_content:
                    with open(full_path, 'w', encoding='utf-8') as file:
                        file.write(modified_content)

    @staticmethod
    def generate_form_or_table(serializer_data, initial_tag, template_file):
        data = {}
        for key in serializer_data:
            text = format_with_jinja(
                serializer_data[key],
                template_file
            )
            tag = f"// TAG: {key}{initial_tag}"
            data[tag] = text.strip()
            print(text)
        return data

    @staticmethod
    def get_serializer_list(files):
        serializers_list = []
        for file_path in files["serializers"]:
            module_name = os.path.splitext(os.path.basename(file_path))[0]
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and (
                        issubclass(obj, serializers.Serializer) or issubclass(obj, serializers.ModelSerializer)):
                    serializers_list.append(obj)
        return serializers_list

    def get_serializer_data(self, serializer_list):
        serializer_fields = {}
        for serializer in serializer_list:
            serializer_instance = serializer()
            model = getattr(serializer.Meta, 'model', None) if hasattr(serializer, 'Meta') and hasattr(serializer.Meta,
                                                                                                       'model') else None
            model_name = model.__name__ if model else None
            app_name = model._meta.app_label if model else None
            serializer_name = f"{serializer.__name__}".replace("Serializer", "")

            if hasattr(serializer_instance, 'fields'):
                fields = serializer_instance.fields
                field_objects = [
                    {
                        'name': field_name,
                        'type': type(field).__name__,
                        'required': field.required,
                        'write_only': field.write_only,
                        'read_only': field.read_only,
                        'nullable': field.allow_null,
                        'max_length': getattr(field, 'max_length', None),
                        'size': getattr(field, 'size', None),
                        'help_text': getattr(field, 'help_text', None),
                        'is_primary_key': field.source in ['id', 'pk'],
                    }
                    for field_name, field in fields.items()
                ]
                serializer_fields[serializer_name] = {
                    "fields": field_objects,
                    "model_name": model_name,
                    "serializer_name": serializer_name,
                    "app_name": app_name,
                    "formly_type_map": self.formly_type_map,
                    "formly_props_type_map": self.formly_props_type_map,
                }
        return serializer_fields

    def get_models_and_serializer_files(self):
        project_root = os.getcwd()
        apps = self.get_apps(project_root)
        models = []
        serializers = []
        for app in apps:
            models_path = os.path.join(project_root, app, 'models')
            serializers_path = os.path.join(project_root, app, 'serializers')

            if os.path.isdir(models_path):
                models.extend(self.get_python_files(models_path))
            elif os.path.exists(models_path + '.py'):
                models.append(models_path + '.py')

            if os.path.isdir(serializers_path):
                serializers.extend(self.get_python_files(serializers_path))
            elif os.path.exists(serializers_path + '.py'):
                serializers.append(serializers_path + '.py')

        return {
            "models": models,
            "serializers": serializers
        }

    @staticmethod
    def get_apps(project_root) -> list[str]:
        apps = []
        for root, dirs, files in os.walk(project_root):
            if 'apps.py' in files:
                app_path = os.path.relpath(root, project_root)
                apps.append(str(app_path))
        return apps

    @staticmethod
    def get_python_files(directory):
        python_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        return python_files

    def check_client_folder(self):
        if not os.path.exists(self.file_path) or not os.path.isdir(self.file_path):
            raise FileNotFoundError(f"The folder '{self.file_path}' does not exist.")
        if os.path.abspath(self.file_path) == os.path.abspath(os.sep) or not os.listdir(self.file_path):
            raise ValueError(f"The folder '{self.file_path}' is either root or empty.")
