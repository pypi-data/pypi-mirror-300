from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.dash_nav_item_variant_type_0 import DashNavItemVariantType0
from ..types import UNSET, Unset

T = TypeVar("T", bound="DashNavItem")


@_attrs_define
class DashNavItem:
    """菜单导航
    目前 以列表的方式表示，
    以后升级为树

        Attributes:
            title (Union[None, Unset, str]):
            label (Union[None, Unset, str]):
            icon (Union[None, Unset, str]):
            url (Union[None, Unset, str]):
            variant (Union[DashNavItemVariantType0, None, Unset]):  Default: DashNavItemVariantType0.DEFAULT.
            tooltip (Union[None, Unset, str]):
    """

    title: Union[None, Unset, str] = UNSET
    label: Union[None, Unset, str] = UNSET
    icon: Union[None, Unset, str] = UNSET
    url: Union[None, Unset, str] = UNSET
    variant: Union[DashNavItemVariantType0, None, Unset] = DashNavItemVariantType0.DEFAULT
    tooltip: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        title: Union[None, Unset, str]
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        label: Union[None, Unset, str]
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        icon: Union[None, Unset, str]
        if isinstance(self.icon, Unset):
            icon = UNSET
        else:
            icon = self.icon

        url: Union[None, Unset, str]
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        variant: Union[None, Unset, str]
        if isinstance(self.variant, Unset):
            variant = UNSET
        elif isinstance(self.variant, DashNavItemVariantType0):
            variant = self.variant.value
        else:
            variant = self.variant

        tooltip: Union[None, Unset, str]
        if isinstance(self.tooltip, Unset):
            tooltip = UNSET
        else:
            tooltip = self.tooltip

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if label is not UNSET:
            field_dict["label"] = label
        if icon is not UNSET:
            field_dict["icon"] = icon
        if url is not UNSET:
            field_dict["url"] = url
        if variant is not UNSET:
            field_dict["variant"] = variant
        if tooltip is not UNSET:
            field_dict["tooltip"] = tooltip

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_title(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_icon(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        icon = _parse_icon(d.pop("icon", UNSET))

        def _parse_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        url = _parse_url(d.pop("url", UNSET))

        def _parse_variant(data: object) -> Union[DashNavItemVariantType0, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                variant_type_0 = DashNavItemVariantType0(data)

                return variant_type_0
            except:  # noqa: E722
                pass
            return cast(Union[DashNavItemVariantType0, None, Unset], data)

        variant = _parse_variant(d.pop("variant", UNSET))

        def _parse_tooltip(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tooltip = _parse_tooltip(d.pop("tooltip", UNSET))

        dash_nav_item = cls(
            title=title,
            label=label,
            icon=icon,
            url=url,
            variant=variant,
            tooltip=tooltip,
        )

        dash_nav_item.additional_properties = d
        return dash_nav_item

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
