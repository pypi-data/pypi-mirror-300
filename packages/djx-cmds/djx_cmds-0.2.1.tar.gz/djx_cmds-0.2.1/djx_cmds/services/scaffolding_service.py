import os

import inflection
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import ManyToOneRel

from djx_cmds.format_with_jinja import format_with_jinja
from djx_cmds.services.import_object import ImportObject


class ScaffoldingService:

    def __init__(self, name, actions):
        self.name = name
        self.actions = actions

    def run(self):
        model_data = ImportObject().import_model(self.name)
        model_name = model_data['name']
        model_module = model_data['module']

        model = ImportObject().get_model(model_name)
        app_name = ImportObject.get_app(model)
        fields = ImportObject().get_model_fields(model)
        many_to_one_relations = self.get_many_to_one_relations(fields)
        user_fields = self.get_user_model_fields(fields)

        self.create_serializer(model_name, model_module, fields, user_fields, many_to_one_relations, app_name)
        self.create_views(model_name, model_module, fields, user_fields, many_to_one_relations, app_name)

    def create_serializer(self, model_name, model_module, fields, user_fields, many_to_one_relations, app_name):

        serializer_content = format_with_jinja(
            {
                'model_name': model_name,
                "methods": list(self.actions),
                "fields": fields,
                "model_module": model_module,
                "user_fields": user_fields,
                "many_to_one_relations": many_to_one_relations
            },
            'serializer.txt'
        )

        serializer_file_name = inflection.underscore(f"{model_name}_serializers.py")

        serializer_file_path = os.path.join(settings.BASE_DIR, app_name, 'serializers', serializer_file_name)

        self.create_file(file_path=serializer_file_path, file_content=serializer_content)

    @staticmethod
    def create_file(file_path, file_content, mode='w'):
        dirname = os.path.dirname(file_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(file_path, mode, encoding='utf-8') as f:
            f.write(file_content)

    @staticmethod
    def create_urls(app_name, model_name):
        dash = inflection.dasherize(inflection.underscore(model_name))
        register = f"router.register('{dash}', {model_name}ViewSet, basename='{dash}')"
        file_path = os.path.join(settings.BASE_DIR, app_name, 'urls.py')
        with open(file_path, 'r') as f:
            content = f.read()
        tag = "# registration"
        import_str = f"from {app_name}.views.{inflection.underscore(model_name)}_views import {model_name}ViewSet"
        content = content.replace(f"{tag}", f'{register}\n{tag}')
        content = f"{import_str}\n{content}"
        with open(file_path, 'w') as f:
            content = f.write(content)

    @staticmethod
    def get_user_model_fields(fields):
        UserModel = get_user_model()
        return [element["name"] for element in fields if element["cls"].related_model == UserModel]

    @staticmethod
    def get_many_to_one_relations(array):
        many_relations = []
        for item in array:
            if isinstance(item['cls'], ManyToOneRel):
                many_relations.append(item['name'])
        return many_relations

    def create_views(self, model_name, model_module, fields, user_fields, many_to_one_relations, app_name):
        model = ImportObject().get_model(model_name)
        app_name = ImportObject.get_app(model)
        view_content = format_with_jinja(
            {
                "app_name": app_name,
                'model_name': model_name,
                'model_name_snake_case': inflection.underscore(model_name),
                'actions': self.actions,
                "methods": list(self.actions),
                "fields": fields,
                "model_module": model_module,
                "user_fields": user_fields,
                "many_to_one_relations": many_to_one_relations

            },
            'view.txt')

        view_file_name = inflection.underscore(f"{model_name}_views.py")

        view_file_path = os.path.join(settings.BASE_DIR, app_name, 'views', view_file_name)
        self.create_file(file_path=view_file_path, file_content=view_content)
        self.create_urls(app_name, model_name)
