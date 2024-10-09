from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.page_meta_author import PageMetaAuthor


T = TypeVar("T", bound="PageMetaResponse")


@_attrs_define
class PageMetaResponse:
    """对应前端页面的 page meta 信息

    Attributes:
        title (Union[None, Unset, str]):  Default: ''.
        metadata_base (Union[Unset, str]):  Default: ''.
        description (Union[Unset, str]):  Default: ''.
        keywords (Union[Unset, List[str]]):
        authors (Union[Unset, List['PageMetaAuthor']]):
        creator (Union[Unset, str]):  Default: ''.
        manifest (Union[Unset, str]):  Default: ''.
    """

    title: Union[None, Unset, str] = ""
    metadata_base: Union[Unset, str] = ""
    description: Union[Unset, str] = ""
    keywords: Union[Unset, List[str]] = UNSET
    authors: Union[Unset, List["PageMetaAuthor"]] = UNSET
    creator: Union[Unset, str] = ""
    manifest: Union[Unset, str] = ""
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        title: Union[None, Unset, str]
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        metadata_base = self.metadata_base

        description = self.description

        keywords: Union[Unset, List[str]] = UNSET
        if not isinstance(self.keywords, Unset):
            keywords = self.keywords

        authors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.authors, Unset):
            authors = []
            for authors_item_data in self.authors:
                authors_item = authors_item_data.to_dict()
                authors.append(authors_item)

        creator = self.creator

        manifest = self.manifest

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if metadata_base is not UNSET:
            field_dict["metadataBase"] = metadata_base
        if description is not UNSET:
            field_dict["description"] = description
        if keywords is not UNSET:
            field_dict["keywords"] = keywords
        if authors is not UNSET:
            field_dict["authors"] = authors
        if creator is not UNSET:
            field_dict["creator"] = creator
        if manifest is not UNSET:
            field_dict["manifest"] = manifest

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.page_meta_author import PageMetaAuthor

        d = src_dict.copy()

        def _parse_title(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        title = _parse_title(d.pop("title", UNSET))

        metadata_base = d.pop("metadataBase", UNSET)

        description = d.pop("description", UNSET)

        keywords = cast(List[str], d.pop("keywords", UNSET))

        authors = []
        _authors = d.pop("authors", UNSET)
        for authors_item_data in _authors or []:
            authors_item = PageMetaAuthor.from_dict(authors_item_data)

            authors.append(authors_item)

        creator = d.pop("creator", UNSET)

        manifest = d.pop("manifest", UNSET)

        page_meta_response = cls(
            title=title,
            metadata_base=metadata_base,
            description=description,
            keywords=keywords,
            authors=authors,
            creator=creator,
            manifest=manifest,
        )

        page_meta_response.additional_properties = d
        return page_meta_response

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
