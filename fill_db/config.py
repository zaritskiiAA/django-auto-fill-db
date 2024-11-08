from typing import Iterable

from django.conf import settings as django_settings
from django.utils.functional import cached_property


class Config:

    _apps_exclude = frozenset(
        [
            "admin", "contenttypes", "auth", "group_permissions", 
            "group", "user_groups", "user_user_permissions",
            "sessions", "messages", "staticfiles",
        ]
    )

    def __init__(self):

        self.conf = getattr(django_settings, "AUTO_FILL_CONFIG", {})
        
    @cached_property
    def apps_exclude(self):

        if exclude := self.conf.get("apps_exclude"):
            assert isinstance(exclude, Iterable), "'apps_exclude' in config must be iterable"
            exclude = set(exclude)
            for app in self._apps_exclude:
                exclude.add(app)
            return frozenset(exclude)
        return self._apps_exclude
    
    @cached_property
    def tables_exclude(self):

        tables_exc = {}

        if exclude := self.conf.get("tables_exclude"):
            assert isinstance(exclude, dict), "'tables_exclude' in config must be dict instance"
            for app, tables in exclude.items():
                assert isinstance(tables, Iterable), "models in 'tables exclude' must be iterable"
                tables_exc[app] = set(tables)
        return tables_exc