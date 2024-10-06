import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="BlogPostDetailResponse")


@_attrs_define
class BlogPostDetailResponse:
    """
    Attributes:
        id (str):
        title (str):
        content (str):
        tags (List[str]):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        author (Union[None, str]):
    """

    id: str
    title: str
    content: str
    tags: List[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    author: Union[None, str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        title = self.title

        content = self.content

        tags = self.tags

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        author: Union[None, str]
        author = self.author

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "title": title,
                "content": content,
                "tags": tags,
                "created_at": created_at,
                "updated_at": updated_at,
                "author": author,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        title = d.pop("title")

        content = d.pop("content")

        tags = cast(List[str], d.pop("tags"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_author(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        author = _parse_author(d.pop("author"))

        blog_post_detail_response = cls(
            id=id,
            title=title,
            content=content,
            tags=tags,
            created_at=created_at,
            updated_at=updated_at,
            author=author,
        )

        blog_post_detail_response.additional_properties = d
        return blog_post_detail_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
