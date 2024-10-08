from enum import Enum


class ThreadFormVariant(str, Enum):
    CMDK = "cmdk"
    DEFAULT = "default"
    SINGLE_SELECT = "single_select"

    def __str__(self) -> str:
        return str(self.value)
