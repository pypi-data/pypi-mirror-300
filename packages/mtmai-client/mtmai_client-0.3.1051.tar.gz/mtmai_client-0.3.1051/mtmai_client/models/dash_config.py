from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dash_nav_item import DashNavItem


T = TypeVar("T", bound="DashConfig")


@_attrs_define
class DashConfig:
    """管理面板的后台配置

    Attributes:
        logo (Union[None, Unset, str]):
        path_prefix (Union[None, Unset, str]):  Default: '/'.
        nav_menus (Union[List['DashNavItem'], None, Unset]):
        login_url (Union[Unset, str]):  Default: '/auth/login'.
        theme (Union[None, Unset, str]):  Default: 'light'.
        layout (Union[None, Unset, str]):  Default: 'default'.
    """

    logo: Union[None, Unset, str] = UNSET
    path_prefix: Union[None, Unset, str] = "/"
    nav_menus: Union[List["DashNavItem"], None, Unset] = UNSET
    login_url: Union[Unset, str] = "/auth/login"
    theme: Union[None, Unset, str] = "light"
    layout: Union[None, Unset, str] = "default"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        logo: Union[None, Unset, str]
        if isinstance(self.logo, Unset):
            logo = UNSET
        else:
            logo = self.logo

        path_prefix: Union[None, Unset, str]
        if isinstance(self.path_prefix, Unset):
            path_prefix = UNSET
        else:
            path_prefix = self.path_prefix

        nav_menus: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.nav_menus, Unset):
            nav_menus = UNSET
        elif isinstance(self.nav_menus, list):
            nav_menus = []
            for nav_menus_type_0_item_data in self.nav_menus:
                nav_menus_type_0_item = nav_menus_type_0_item_data.to_dict()
                nav_menus.append(nav_menus_type_0_item)

        else:
            nav_menus = self.nav_menus

        login_url = self.login_url

        theme: Union[None, Unset, str]
        if isinstance(self.theme, Unset):
            theme = UNSET
        else:
            theme = self.theme

        layout: Union[None, Unset, str]
        if isinstance(self.layout, Unset):
            layout = UNSET
        else:
            layout = self.layout

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if logo is not UNSET:
            field_dict["logo"] = logo
        if path_prefix is not UNSET:
            field_dict["pathPrefix"] = path_prefix
        if nav_menus is not UNSET:
            field_dict["navMenus"] = nav_menus
        if login_url is not UNSET:
            field_dict["loginUrl"] = login_url
        if theme is not UNSET:
            field_dict["theme"] = theme
        if layout is not UNSET:
            field_dict["layout"] = layout

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.dash_nav_item import DashNavItem

        d = src_dict.copy()

        def _parse_logo(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        logo = _parse_logo(d.pop("logo", UNSET))

        def _parse_path_prefix(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        path_prefix = _parse_path_prefix(d.pop("pathPrefix", UNSET))

        def _parse_nav_menus(data: object) -> Union[List["DashNavItem"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                nav_menus_type_0 = []
                _nav_menus_type_0 = data
                for nav_menus_type_0_item_data in _nav_menus_type_0:
                    nav_menus_type_0_item = DashNavItem.from_dict(nav_menus_type_0_item_data)

                    nav_menus_type_0.append(nav_menus_type_0_item)

                return nav_menus_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["DashNavItem"], None, Unset], data)

        nav_menus = _parse_nav_menus(d.pop("navMenus", UNSET))

        login_url = d.pop("loginUrl", UNSET)

        def _parse_theme(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        theme = _parse_theme(d.pop("theme", UNSET))

        def _parse_layout(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        layout = _parse_layout(d.pop("layout", UNSET))

        dash_config = cls(
            logo=logo,
            path_prefix=path_prefix,
            nav_menus=nav_menus,
            login_url=login_url,
            theme=theme,
            layout=layout,
        )

        dash_config.additional_properties = d
        return dash_config

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
