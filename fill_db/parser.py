from django.utils.functional import cached_property
from django.apps import apps as django_apps

from .config import Config


class Parser:

    @cached_property
    def config(self):
        return Config()

    @cached_property
    def tables_to_parse(self):
        all_models = {}

        for app, tables in django_apps.all_models.items():

            if tables and app not in self.config.apps_exclude:
                if table_exclude := self.config.tables_exclude.get(app):
                    tables = {t: obj for t, obj in tables.items() if t not in table_exclude}
                all_models[app] = tables
        return all_models

    def parse(self)
        pass
        
