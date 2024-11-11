from django.core.management.base import BaseCommand, CommandError

from fill_db.parser import Parser
from fill_db.handers import MessageHandler


class Command(BaseCommand):
    help = 'Generated django model objects.'

    def add_arguments(self, parser):
        parser.add_argument("init", type=bool)

    def handle(self, *args, **options):

        MessageHandler._stdout = self.stdout
        parser = Parser()

        if options.get("init"):
            parser.parse()
        
