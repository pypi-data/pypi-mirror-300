from enum import Enum


class ThreadUIStateInputPositionType0(str, Enum):
    BOTTOM = "bottom"
    INLINE = "inline"

    def __str__(self) -> str:
        return str(self.value)
