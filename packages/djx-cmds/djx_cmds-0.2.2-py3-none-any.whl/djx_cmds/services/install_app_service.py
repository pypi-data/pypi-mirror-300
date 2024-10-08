import os
from pathlib import Path

from django.conf import settings


class InstallAppService:

    def __init__(self, app_name):
        self.app_name = app_name

    def run(self):
        self.install_app()
        self.install_url()

    def install_app(self):
        install_app_tag = "# installAppRegistration"
        replace_value = f'"{self.app_name}",\n\t{install_app_tag}'
        settings_module = os.environ.get('DJANGO_SETTINGS_MODULE')
        settings_path = Path(settings_module.replace('.', '/') + '.py')
        self.find_and_replace(settings_path, install_app_tag, replace_value)

    def install_url(self):
        install_url_tag = "# AppUrlRegistration"
        urls_module = settings.ROOT_URLCONF
        url_path = Path(urls_module.replace('.', '/') + '.py')

        replace_value = f"path('api/', include('{self.app_name}.urls')),\n\t{install_url_tag}"
        self.find_and_replace(url_path, install_url_tag, replace_value)

    @staticmethod
    def find_and_replace(file_path, tag, replace_value):
        with open(file_path, 'r') as file:
            content = file.read()
        updated_content = content.replace(tag, replace_value)
        with open(file_path, 'w') as file:
            file.write(updated_content)
