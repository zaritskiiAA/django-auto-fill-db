from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Generated django model object.'

    def add_arguments(self, parser):
        parser.add_argument("init", type=bool)

    def handle(self, *args, **options):
        pass