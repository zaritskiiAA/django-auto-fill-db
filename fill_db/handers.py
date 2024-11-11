from typing import Optional

from django.core.management.base import OutputWrapper

from .exceptions import IOWrapperDoesNotSet


class MessageHandler:

    _stdout: Optional[OutputWrapper] = None

    @property
    def stdout(self):
        if self._stdout:
            return self._stdout
        raise IOWrapperDoesNotSet("you must set django command outputwrapper to MessageHandler attr")
