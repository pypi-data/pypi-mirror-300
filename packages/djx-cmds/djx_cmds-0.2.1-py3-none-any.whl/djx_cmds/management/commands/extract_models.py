from django.core.management.base import BaseCommand

from djx_cmds.services.clean_migration import CleanMigration
from djx_cmds.services.extract_models_service import ExtractModelsService
from djx_cmds.services.scaffolding_service import ScaffoldingService


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        content = ExtractModelsService().run()
        self.stdout.write(content)
