from enum import Enum


class DashNavItemVariantType0(str, Enum):
    DEFAULT = "default"
    GHOST = "ghost"

    def __str__(self) -> str:
        return str(self.value)
