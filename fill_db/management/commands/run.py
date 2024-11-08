from django.core.management.base import BaseCommand, CommandError

from fill_db.parser import Parser


class Command(BaseCommand):
    help = 'Generated django model object.'

    def add_arguments(self, parser):
        parser.add_argument("init", type=bool)

    def handle(self, *args, **options):
        if options.get("init"):
            Parser().parse()