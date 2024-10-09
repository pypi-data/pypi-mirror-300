from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copilot_screen import CopilotScreen


T = TypeVar("T", bound="ChatBotUiStateResponse")


@_attrs_define
class ChatBotUiStateResponse:
    """
    Attributes:
        agent (Union[None, Unset, str]):
        layout (Union[None, Unset, str]):
        theme (Union[None, Unset, str]):
        is_open (Union[Unset, bool]):  Default: False.
        fab_display_text (Union[None, Unset, str]):
        fab_display_icon (Union[None, Unset, str]):
        fab_display_color (Union[None, Unset, str]):
        fab_display_action (Union[None, Unset, str]):
        is_open_data_view (Union[Unset, bool]):  Default: False.
        activate_view_name (Union[None, Unset, str]):
        activate_chat_profile_id (Union[None, Unset, str]):
        screens (Union[Unset, List['CopilotScreen']]):
    """

    agent: Union[None, Unset, str] = UNSET
    layout: Union[None, Unset, str] = UNSET
    theme: Union[None, Unset, str] = UNSET
    is_open: Union[Unset, bool] = False
    fab_display_text: Union[None, Unset, str] = UNSET
    fab_display_icon: Union[None, Unset, str] = UNSET
    fab_display_color: Union[None, Unset, str] = UNSET
    fab_display_action: Union[None, Unset, str] = UNSET
    is_open_data_view: Union[Unset, bool] = False
    activate_view_name: Union[None, Unset, str] = UNSET
    activate_chat_profile_id: Union[None, Unset, str] = UNSET
    screens: Union[Unset, List["CopilotScreen"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        agent: Union[None, Unset, str]
        if isinstance(self.agent, Unset):
            agent = UNSET
        else:
            agent = self.agent

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

        is_open = self.is_open

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

        is_open_data_view = self.is_open_data_view

        activate_view_name: Union[None, Unset, str]
        if isinstance(self.activate_view_name, Unset):
            activate_view_name = UNSET
        else:
            activate_view_name = self.activate_view_name

        activate_chat_profile_id: Union[None, Unset, str]
        if isinstance(self.activate_chat_profile_id, Unset):
            activate_chat_profile_id = UNSET
        else:
            activate_chat_profile_id = self.activate_chat_profile_id

        screens: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.screens, Unset):
            screens = []
            for screens_item_data in self.screens:
                screens_item = screens_item_data.to_dict()
                screens.append(screens_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agent is not UNSET:
            field_dict["agent"] = agent
        if layout is not UNSET:
            field_dict["layout"] = layout
        if theme is not UNSET:
            field_dict["theme"] = theme
        if is_open is not UNSET:
            field_dict["isOpen"] = is_open
        if fab_display_text is not UNSET:
            field_dict["fabDisplayText"] = fab_display_text
        if fab_display_icon is not UNSET:
            field_dict["fabDisplayIcon"] = fab_display_icon
        if fab_display_color is not UNSET:
            field_dict["fabDisplayColor"] = fab_display_color
        if fab_display_action is not UNSET:
            field_dict["fabDisplayAction"] = fab_display_action
        if is_open_data_view is not UNSET:
            field_dict["isOpenDataView"] = is_open_data_view
        if activate_view_name is not UNSET:
            field_dict["activateViewName"] = activate_view_name
        if activate_chat_profile_id is not UNSET:
            field_dict["activateChatProfileId"] = activate_chat_profile_id
        if screens is not UNSET:
            field_dict["screens"] = screens

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.copilot_screen import CopilotScreen

        d = src_dict.copy()

        def _parse_agent(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        agent = _parse_agent(d.pop("agent", UNSET))

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

        is_open = d.pop("isOpen", UNSET)

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

        is_open_data_view = d.pop("isOpenDataView", UNSET)

        def _parse_activate_view_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        activate_view_name = _parse_activate_view_name(d.pop("activateViewName", UNSET))

        def _parse_activate_chat_profile_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        activate_chat_profile_id = _parse_activate_chat_profile_id(d.pop("activateChatProfileId", UNSET))

        screens = []
        _screens = d.pop("screens", UNSET)
        for screens_item_data in _screens or []:
            screens_item = CopilotScreen.from_dict(screens_item_data)

            screens.append(screens_item)

        chat_bot_ui_state_response = cls(
            agent=agent,
            layout=layout,
            theme=theme,
            is_open=is_open,
            fab_display_text=fab_display_text,
            fab_display_icon=fab_display_icon,
            fab_display_color=fab_display_color,
            fab_display_action=fab_display_action,
            is_open_data_view=is_open_data_view,
            activate_view_name=activate_view_name,
            activate_chat_profile_id=activate_chat_profile_id,
            screens=screens,
        )

        chat_bot_ui_state_response.additional_properties = d
        return chat_bot_ui_state_response

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
