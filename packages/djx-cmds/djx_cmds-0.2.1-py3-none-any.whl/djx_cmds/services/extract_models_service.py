import os


class ExtractModelsService:

    def run(self):
        files = self.get_models_and_serializer_files()
        result = []
        for file_path in files:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                if content:  # Ignore empty files
                    relative_path = os.path.relpath(file_path, os.getcwd())
                    result.append(f"# {relative_path}\n\n{content}\n")
        response = "\n".join(result)
        return response

    def get_models_and_serializer_files(self):
        project_root = os.getcwd()
        apps = self.get_apps(project_root)
        all_models_and_serializers = []

        for app in apps:
            models_path = os.path.join(project_root, app, 'models')
            serializers_path = os.path.join(project_root, app, 'serializers')

            if os.path.isdir(models_path):
                all_models_and_serializers.extend(self.get_python_files(models_path))
            elif os.path.exists(models_path + '.py'):
                all_models_and_serializers.append(models_path + '.py')

            if os.path.isdir(serializers_path):
                all_models_and_serializers.extend(self.get_python_files(serializers_path))
            elif os.path.exists(serializers_path + '.py'):
                all_models_and_serializers.append(serializers_path + '.py')

        return all_models_and_serializers

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
