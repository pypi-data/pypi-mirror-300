from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SiteHostItemPublic")


@_attrs_define
class SiteHostItemPublic:
    """
    Attributes:
        domain (str):
        site_id (str):
        id (str):
        is_default (Union[Unset, bool]):  Default: False.
        is_https (Union[Unset, bool]):  Default: False.
    """

    domain: str
    site_id: str
    id: str
    is_default: Union[Unset, bool] = False
    is_https: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        domain = self.domain

        site_id = self.site_id

        id = self.id

        is_default = self.is_default

        is_https = self.is_https

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "domain": domain,
                "site_id": site_id,
                "id": id,
            }
        )
        if is_default is not UNSET:
            field_dict["is_default"] = is_default
        if is_https is not UNSET:
            field_dict["is_https"] = is_https

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        domain = d.pop("domain")

        site_id = d.pop("site_id")

        id = d.pop("id")

        is_default = d.pop("is_default", UNSET)

        is_https = d.pop("is_https", UNSET)

        site_host_item_public = cls(
            domain=domain,
            site_id=site_id,
            id=id,
            is_default=is_default,
            is_https=is_https,
        )

        site_host_item_public.additional_properties = d
        return site_host_item_public

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
