from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.thread_ui_state_fab_display_position_type_0 import ThreadUIStateFabDisplayPositionType0
from ..models.thread_ui_state_input_position_type_0 import ThreadUIStateInputPositionType0
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copilot_screen import CopilotScreen


T = TypeVar("T", bound="ThreadUIState")


@_attrs_define
class ThreadUIState:
    """ThreadView 的UI 状态

    Attributes:
        enable_chat (Union[None, Unset, bool]):  Default: False.
        enable_scroll_to_bottom (Union[Unset, bool]):  Default: True.
        title (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        icons (Union[None, Unset, str]):
        layout (Union[None, Unset, str]):
        theme (Union[None, Unset, str]):
        is_open (Union[None, Unset, bool]):
        screens (Union[Unset, List['CopilotScreen']]):
        activate_view_name (Union[None, Unset, str]):  Default: '/'.
        input_position (Union[None, ThreadUIStateInputPositionType0, Unset]):  Default:
            ThreadUIStateInputPositionType0.BOTTOM.
        fab_enabled (Union[Unset, bool]):  Default: True.
        fab_icon (Union[None, Unset, str]):
        fab_action (Union[None, Unset, str]):
        fab_display_text (Union[None, Unset, str]):
        fab_display_icon (Union[None, Unset, str]):
        fab_display_color (Union[None, Unset, str]):
        fab_display_action (Union[None, Unset, str]):
        fab_display_position (Union[None, ThreadUIStateFabDisplayPositionType0, Unset]):  Default:
            ThreadUIStateFabDisplayPositionType0.BOTTOM.
    """

    enable_chat: Union[None, Unset, bool] = False
    enable_scroll_to_bottom: Union[Unset, bool] = True
    title: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    icons: Union[None, Unset, str] = UNSET
    layout: Union[None, Unset, str] = UNSET
    theme: Union[None, Unset, str] = UNSET
    is_open: Union[None, Unset, bool] = UNSET
    screens: Union[Unset, List["CopilotScreen"]] = UNSET
    activate_view_name: Union[None, Unset, str] = "/"
    input_position: Union[None, ThreadUIStateInputPositionType0, Unset] = ThreadUIStateInputPositionType0.BOTTOM
    fab_enabled: Union[Unset, bool] = True
    fab_icon: Union[None, Unset, str] = UNSET
    fab_action: Union[None, Unset, str] = UNSET
    fab_display_text: Union[None, Unset, str] = UNSET
    fab_display_icon: Union[None, Unset, str] = UNSET
    fab_display_color: Union[None, Unset, str] = UNSET
    fab_display_action: Union[None, Unset, str] = UNSET
    fab_display_position: Union[None, ThreadUIStateFabDisplayPositionType0, Unset] = (
        ThreadUIStateFabDisplayPositionType0.BOTTOM
    )
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        enable_chat: Union[None, Unset, bool]
        if isinstance(self.enable_chat, Unset):
            enable_chat = UNSET
        else:
            enable_chat = self.enable_chat

        enable_scroll_to_bottom = self.enable_scroll_to_bottom

        title: Union[None, Unset, str]
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        icons: Union[None, Unset, str]
        if isinstance(self.icons, Unset):
            icons = UNSET
        else:
            icons = self.icons

        layout: Union[None, Unset, str]
        if isinstance(self.layout, Unset):
            layout = UNSET
        else:
            layout = self.layout

        theme: Union[None, Unset, str]
        if isinstance(self.theme, Unset):
            theme = UNSET
        else:
            theme = self.theme

        is_open: Union[None, Unset, bool]
        if isinstance(self.is_open, Unset):
            is_open = UNSET
        else:
            is_open = self.is_open

        screens: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.screens, Unset):
            screens = []
            for screens_item_data in self.screens:
                screens_item = screens_item_data.to_dict()
                screens.append(screens_item)

        activate_view_name: Union[None, Unset, str]
        if isinstance(self.activate_view_name, Unset):
            activate_view_name = UNSET
        else:
            activate_view_name = self.activate_view_name

        input_position: Union[None, Unset, str]
        if isinstance(self.input_position, Unset):
            input_position = UNSET
        elif isinstance(self.input_position, ThreadUIStateInputPositionType0):
            input_position = self.input_position.value
        else:
            input_position = self.input_position

        fab_enabled = self.fab_enabled

        fab_icon: Union[None, Unset, str]
        if isinstance(self.fab_icon, Unset):
            fab_icon = UNSET
        else:
            fab_icon = self.fab_icon

        fab_action: Union[None, Unset, str]
        if isinstance(self.fab_action, Unset):
            fab_action = UNSET
        else:
            fab_action = self.fab_action

        fab_display_text: Union[None, Unset, str]
        if isinstance(self.fab_display_text, Unset):
            fab_display_text = UNSET
        else:
            fab_display_text = self.fab_display_text

        fab_display_icon: Union[None, Unset, str]
        if isinstance(self.fab_display_icon, Unset):
            fab_display_icon = UNSET
        else:
            fab_display_icon = self.fab_display_icon

        fab_display_color: Union[None, Unset, str]
        if isinstance(self.fab_display_color, Unset):
            fab_display_color = UNSET
        else:
            fab_display_color = self.fab_display_color

        fab_display_action: Union[None, Unset, str]
        if isinstance(self.fab_display_action, Unset):
            fab_display_action = UNSET
        else:
            fab_display_action = self.fab_display_action

        fab_display_position: Union[None, Unset, str]
        if isinstance(self.fab_display_position, Unset):
            fab_display_position = UNSET
        elif isinstance(self.fab_display_position, ThreadUIStateFabDisplayPositionType0):
            fab_display_position = self.fab_display_position.value
        else:
            fab_display_position = self.fab_display_position

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enable_chat is not UNSET:
            field_dict["enableChat"] = enable_chat
        if enable_scroll_to_bottom is not UNSET:
            field_dict["enableScrollToBottom"] = enable_scroll_to_bottom
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if icons is not UNSET:
            field_dict["icons"] = icons
        if layout is not UNSET:
            field_dict["layout"] = layout
        if theme is not UNSET:
            field_dict["theme"] = theme
        if is_open is not UNSET:
            field_dict["isOpen"] = is_open
        if screens is not UNSET:
            field_dict["screens"] = screens
        if activate_view_name is not UNSET:
            field_dict["activateViewName"] = activate_view_name
        if input_position is not UNSET:
            field_dict["inputPosition"] = input_position
        if fab_enabled is not UNSET:
            field_dict["fabEnabled"] = fab_enabled
        if fab_icon is not UNSET:
            field_dict["fabIcon"] = fab_icon
        if fab_action is not UNSET:
            field_dict["fabAction"] = fab_action
        if fab_display_text is not UNSET:
            field_dict["fabDisplayText"] = fab_display_text
        if fab_display_icon is not UNSET:
            field_dict["fabDisplayIcon"] = fab_display_icon
        if fab_display_color is not UNSET:
            field_dict["fabDisplayColor"] = fab_display_color
        if fab_display_action is not UNSET:
            field_dict["fabDisplayAction"] = fab_display_action
        if fab_display_position is not UNSET:
            field_dict["fabDisplayPosition"] = fab_display_position

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.copilot_screen import CopilotScreen

        d = src_dict.copy()

        def _parse_enable_chat(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        enable_chat = _parse_enable_chat(d.pop("enableChat", UNSET))

        enable_scroll_to_bottom = d.pop("enableScrollToBottom", UNSET)

        def _parse_title(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_icons(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        icons = _parse_icons(d.pop("icons", UNSET))

        def _parse_layout(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        layout = _parse_layout(d.pop("layout", UNSET))

        def _parse_theme(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        theme = _parse_theme(d.pop("theme", UNSET))

        def _parse_is_open(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_open = _parse_is_open(d.pop("isOpen", UNSET))

        screens = []
        _screens = d.pop("screens", UNSET)
        for screens_item_data in _screens or []:
            screens_item = CopilotScreen.from_dict(screens_item_data)

            screens.append(screens_item)

        def _parse_activate_view_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        activate_view_name = _parse_activate_view_name(d.pop("activateViewName", UNSET))

        def _parse_input_position(data: object) -> Union[None, ThreadUIStateInputPositionType0, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                input_position_type_0 = ThreadUIStateInputPositionType0(data)

                return input_position_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, ThreadUIStateInputPositionType0, Unset], data)

        input_position = _parse_input_position(d.pop("inputPosition", UNSET))

        fab_enabled = d.pop("fabEnabled", UNSET)

        def _parse_fab_icon(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        fab_icon = _parse_fab_icon(d.pop("fabIcon", UNSET))

        def _parse_fab_action(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        fab_action = _parse_fab_action(d.pop("fabAction", UNSET))

        def _parse_fab_display_text(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        fab_display_text = _parse_fab_display_text(d.pop("fabDisplayText", UNSET))

        def _parse_fab_display_icon(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        fab_display_icon = _parse_fab_display_icon(d.pop("fabDisplayIcon", UNSET))

        def _parse_fab_display_color(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        fab_display_color = _parse_fab_display_color(d.pop("fabDisplayColor", UNSET))

        def _parse_fab_display_action(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        fab_display_action = _parse_fab_display_action(d.pop("fabDisplayAction", UNSET))

        def _parse_fab_display_position(data: object) -> Union[None, ThreadUIStateFabDisplayPositionType0, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                fab_display_position_type_0 = ThreadUIStateFabDisplayPositionType0(data)

                return fab_display_position_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, ThreadUIStateFabDisplayPositionType0, Unset], data)

        fab_display_position = _parse_fab_display_position(d.pop("fabDisplayPosition", UNSET))

        thread_ui_state = cls(
            enable_chat=enable_chat,
            enable_scroll_to_bottom=enable_scroll_to_bottom,
            title=title,
            description=description,
            icons=icons,
            layout=layout,
            theme=theme,
            is_open=is_open,
            screens=screens,
            activate_view_name=activate_view_name,
            input_position=input_position,
            fab_enabled=fab_enabled,
            fab_icon=fab_icon,
            fab_action=fab_action,
            fab_display_text=fab_display_text,
            fab_display_icon=fab_display_icon,
            fab_display_color=fab_display_color,
            fab_display_action=fab_display_action,
            fab_display_position=fab_display_position,
        )

        thread_ui_state.additional_properties = d
        return thread_ui_state

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
