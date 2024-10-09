from enum import Enum


class ThreadUIStateFabDisplayPositionType0(str, Enum):
    BOTTOM = "bottom"
    TOP = "top"

    def __str__(self) -> str:
        return str(self.value)
