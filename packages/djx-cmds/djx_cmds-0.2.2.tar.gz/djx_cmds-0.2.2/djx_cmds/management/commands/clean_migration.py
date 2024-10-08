from django.core.management.base import BaseCommand

from djx_cmds.services.clean_migration import CleanMigration
from djx_cmds.services.scaffolding_service import ScaffoldingService


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, help='name')

    def handle(self, *args, **options):
        name = options['name']
        CleanMigration(name).run()
