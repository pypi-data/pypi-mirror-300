from enum import Enum


class InputWidgetBaseTypeType0(str, Enum):
    ARRAY = "array"
    BOOLEAN = "boolean"
    NUMBER = "number"
    OBJECT = "object"
    SELECT = "select"
    SLIDER = "slider"
    STRING = "string"
    SWITCH = "switch"
    TAGS = "tags"
    TEXTAREA = "textarea"

    def __str__(self) -> str:
        return str(self.value)
