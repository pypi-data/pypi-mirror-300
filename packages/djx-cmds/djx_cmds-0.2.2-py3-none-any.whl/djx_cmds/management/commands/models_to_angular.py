from django.core.management.base import BaseCommand
from djx_cmds.services.models_to_angular_service import ModelsToAngular


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument(
            '--file_path',
            type=str,
            help='The path to the directory or file',
            required=True
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        ModelsToAngular(file_path).run()
