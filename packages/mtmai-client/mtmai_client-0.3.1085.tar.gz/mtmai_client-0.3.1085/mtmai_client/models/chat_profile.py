import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chat_profile_starters_type_0_item import ChatProfileStartersType0Item


T = TypeVar("T", bound="ChatProfile")


@_attrs_define
class ChatProfile:
    """
    Attributes:
        name (str):
        description (str):
        created_at (Union[None, Unset, datetime.datetime]): The date and time the record was created. Field is optional
            and not needed when instantiating a new record. It will be automatically set when the record is created in the
            database.
        updated_at (Union[None, Unset, datetime.datetime]): The date and time the record was updated. Field is optional
            and not needed when instantiating a new record. It will be automatically set when the record is created in the
            database.
        id (Union[Unset, str]):
        icon (Union[None, Unset, str]):
        default (Union[None, Unset, bool]):  Default: False.
        starters (Union[List['ChatProfileStartersType0Item'], None, Unset]):
    """

    name: str
    description: str
    created_at: Union[None, Unset, datetime.datetime] = UNSET
    updated_at: Union[None, Unset, datetime.datetime] = UNSET
    id: Union[Unset, str] = UNSET
    icon: Union[None, Unset, str] = UNSET
    default: Union[None, Unset, bool] = False
    starters: Union[List["ChatProfileStartersType0Item"], None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        description = self.description

        created_at: Union[None, Unset, str]
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: Union[None, Unset, str]
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        id = self.id

        icon: Union[None, Unset, str]
        if isinstance(self.icon, Unset):
            icon = UNSET
        else:
            icon = self.icon

        default: Union[None, Unset, bool]
        if isinstance(self.default, Unset):
            default = UNSET
        else:
            default = self.default

        starters: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.starters, Unset):
            starters = UNSET
        elif isinstance(self.starters, list):
            starters = []
            for starters_type_0_item_data in self.starters:
                starters_type_0_item = starters_type_0_item_data.to_dict()
                starters.append(starters_type_0_item)

        else:
            starters = self.starters

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
            }
        )
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if id is not UNSET:
            field_dict["id"] = id
        if icon is not UNSET:
            field_dict["icon"] = icon
        if default is not UNSET:
            field_dict["default"] = default
        if starters is not UNSET:
            field_dict["starters"] = starters

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.chat_profile_starters_type_0_item import ChatProfileStartersType0Item

        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        def _parse_created_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_updated_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = isoparse(data)

                return updated_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        id = d.pop("id", UNSET)

        def _parse_icon(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        icon = _parse_icon(d.pop("icon", UNSET))

        def _parse_default(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        default = _parse_default(d.pop("default", UNSET))

        def _parse_starters(data: object) -> Union[List["ChatProfileStartersType0Item"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                starters_type_0 = []
                _starters_type_0 = data
                for starters_type_0_item_data in _starters_type_0:
                    starters_type_0_item = ChatProfileStartersType0Item.from_dict(starters_type_0_item_data)

                    starters_type_0.append(starters_type_0_item)

                return starters_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["ChatProfileStartersType0Item"], None, Unset], data)

        starters = _parse_starters(d.pop("starters", UNSET))

        chat_profile = cls(
            name=name,
            description=description,
            created_at=created_at,
            updated_at=updated_at,
            id=id,
            icon=icon,
            default=default,
            starters=starters,
        )

        chat_profile.additional_properties = d
        return chat_profile

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
