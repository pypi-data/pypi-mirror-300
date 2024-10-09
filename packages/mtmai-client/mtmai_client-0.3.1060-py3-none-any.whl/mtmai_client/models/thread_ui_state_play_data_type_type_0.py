from enum import Enum


class ThreadUIStatePlayDataTypeType0(str, Enum):
    DEMOARTICLE = "demoArticle"
    POST = "post"

    def __str__(self) -> str:
        return str(self.value)
