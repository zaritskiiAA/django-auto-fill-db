from typing import Iterable
from collections import defaultdict

from django.conf import settings as django_settings

from .handers import MessageHandler


class Config(MessageHandler):

    _default_apps_exclude = frozenset(
        [
            "admin", "contenttypes", "auth", "group_permissions", 
            "group", "user_groups", "user_user_permissions",
            "sessions", "messages", "staticfiles",
        ]
    )
    _frozen_conf_key = ("ignore_tables",)
    
    def __init__(self):

        self._using_conf = {
            "apps_exclude": [],
            "tables_exclude": {},
            "cache_dir": django_settings.BASE_DIR,
            "cache_filename": "parsed_cache.json",
            "ignore_tables": self.get_ignore_tables(),
        }

        if conf := getattr(django_settings, "AUTO_FILL_CONFIG", None):
            assert isinstance(conf, dict), "AUTO_FILL_CONFIG must be dict instance"
            for k, v in conf.items():
                if k in self.using_conf and k not in self._frozen_conf_key:
                    self.using_conf[k] = v
                else:
                    pass
                    # TODO: вывод в консоль о том, что ключ в конфигах неожидаем.
                    # Добавить сравнение по паттерну, с выводом если есть значительное совпадение.
        self.__post_init__()
     
    def __post_init__(self):
        
        d = {
            "apps_exclude": self.apps_exclude,
            "tables_exclude": self.tables_exclude,
        }
        self.using_conf.update(d)
    
    @property
    def using_conf(self):
        return self._using_conf
    
    @staticmethod
    def get_ignore_tables():
        
        ignore_tables = defaultdict(list)
        if "auth" in django_settings.AUTH_USER_MODEL:
            ignore_tables["auth"].append("user")
        return ignore_tables

    @property
    def apps_exclude(self):

        if self.using_conf["apps_exclude"]:
            assert isinstance(self.using_conf["apps_exclude"], Iterable), "'apps_exclude' in config must be iterable"
            exclude = set(self.using_conf["apps_exclude"])
            for app in self._default_apps_exclude:
                exclude.add(app)
            return frozenset(exclude)
        return self._default_apps_exclude
    
    @property
    def tables_exclude(self):

        tables_exc = {}

        if self.using_conf["tables_exclude"]:
            assert isinstance(self.using_conf["tables_exclude"], dict), "'tables_exclude' in config must be dict instance"
            for app, tables in self.using_conf["tables_exclude"].items():
                assert isinstance(tables, Iterable), "models in 'tables exclude' must be iterable"
                tables_exc[app] = set(tables)
        return tables_exc