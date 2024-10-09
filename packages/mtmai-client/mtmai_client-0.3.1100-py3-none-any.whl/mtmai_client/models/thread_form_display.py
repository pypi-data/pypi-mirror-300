from enum import Enum


class ThreadFormDisplay(str, Enum):
    DRAWER = "drawer"
    INLINE = "inline"
    MODAL = "modal"

    def __str__(self) -> str:
        return str(self.value)
