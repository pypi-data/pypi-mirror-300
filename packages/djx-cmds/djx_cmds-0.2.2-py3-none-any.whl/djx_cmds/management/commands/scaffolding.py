from django.core.management.base import BaseCommand

from djx_cmds.services.scaffolding_service import ScaffoldingService


class Command(BaseCommand):
    help = ''

    def __init__(self):
        super(Command, self).__init__()
        self.available_methods = [
            {'code': 'c', 'action': 'Create'},
            {'code': 'r', 'action': ''},
            {'code': 'u', 'action': 'Update'},
            {'code': 'd', 'action': 'Delete'},
        ]

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, help='name')
        parser.add_argument('--action', type=str, default='r')

    def handle(self, *args, **options):
        name = options['name']
        allowed_actions = options['action']

        ScaffoldingService(name, allowed_actions).run()

