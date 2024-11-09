import os
import json
from typing import Any
from collections import defaultdict

from django.utils.functional import cached_property
from django.apps import apps as django_apps
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model

from .config import Config


class Parser:

    @cached_property
    def config(self) -> Config:
        return Config().using_conf

    @cached_property
    def tables_to_parse(self) -> defaultdict[str, dict[str, Any]]:

        all_models = {}

        for app, tables in django_apps.all_models.items():

            if tables and (app not in self.config["apps_exclude"] or app in self.config["ignore_tables"]):

                if table_exclude := self.config["tables_exclude"].get(app):
                    tables = {t: model_cls for t, model_cls in tables.items() if t not in table_exclude}

                if ignore_tables := self.config["ignore_tables"].get(app):
                    tables = {t: model_cls for t, model_cls in tables.items() if t in ignore_tables}

                all_models[app] = tables
        return all_models
    
    @staticmethod
    def get_django_contenttype_id(model_cls: Model) -> int:
        model_meta = model_cls._meta
        content_object = ContentType.objects.get(
            app_label=model_meta.app_label,
            model=model_meta.model_name,
        )
        return content_object.id
    
    def get_fields(self, model_cls: Model) -> dict[str, Any]:
        meta = model_cls._meta
        simple_fields = {
            "simple": {}, "fk": {}, "mtm": {}, "default_related_name": getattr(meta, "default_related_name", None)
        }
        for field in meta.concrete_fields:

            if not field.primary_key and not hasattr(field, 'through') and not field.related_model:
                simple_fields["simple"].update({field.attname: field.__class__.__name__})
            elif not field.primary_key and field.is_relation:
                simple_fields["fk"].update({field.attname: self.get_django_contenttype_id(field.related_model)})

        for field in meta.many_to_many:
            if not hasattr(field, 'through'):
                simple_fields["mtm"].update(
                    {
                        field.attname: {
                            "contenttype_id":self.get_django_contenttype_id(field.related_model),
                            "related_name": field.related_query_name(),
                        },
                    }
                )
        return simple_fields
    
    def create_tables_map(self) -> dict[str, defaultdict[str, dict[str, Any]]]:

        data = {}

        for app, tables in self.tables_to_parse.items():
            data[app] = defaultdict(dict)
            for t, model_cls in tables.items():
                if not model_cls._meta.auto_created:
                    data[app].update(
                        {
                            t: {
                                "contenttype_id": self.get_django_contenttype_id(model_cls),
                                **self.get_fields(model_cls),
                            }
                        }
                    )
        return data
    
    def generate_json_cache(self, data_to_cache: dict[str, defaultdict[str, dict[str, Any]]]) -> None:

        path = os.path.join(self.config["cache_dir"], self.config["cache_filename"])

        with open(path, "w") as f:
            json.dump(data_to_cache, f, ensure_ascii=False, indent=2)
    
    def parse(self) -> None:
        self.generate_json_cache(self.create_tables_map())

