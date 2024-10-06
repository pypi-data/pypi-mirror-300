from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chat_bot_ui_state_response import ChatBotUiStateResponse
    from ..models.chat_profile import ChatProfile
    from ..models.thread_form import ThreadForm
    from ..models.thread_ui_state import ThreadUIState


T = TypeVar("T", bound="TypesResponse")


@_attrs_define
class TypesResponse:
    """如果使用openapi 生成前端代码，缺少了某些类型，请在这里补充

    Attributes:
        thread_form (Union['ThreadForm', None, Unset]):
        ui_state (Union['ChatBotUiStateResponse', None, Unset]):
        thread_ui_state (Union['ThreadUIState', None, Unset]):
        chat_profile (Union['ChatProfile', None, Unset]):
    """

    thread_form: Union["ThreadForm", None, Unset] = UNSET
    ui_state: Union["ChatBotUiStateResponse", None, Unset] = UNSET
    thread_ui_state: Union["ThreadUIState", None, Unset] = UNSET
    chat_profile: Union["ChatProfile", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.chat_bot_ui_state_response import ChatBotUiStateResponse
        from ..models.chat_profile import ChatProfile
        from ..models.thread_form import ThreadForm
        from ..models.thread_ui_state import ThreadUIState

        thread_form: Union[Dict[str, Any], None, Unset]
        if isinstance(self.thread_form, Unset):
            thread_form = UNSET
        elif isinstance(self.thread_form, ThreadForm):
            thread_form = self.thread_form.to_dict()
        else:
            thread_form = self.thread_form

        ui_state: Union[Dict[str, Any], None, Unset]
        if isinstance(self.ui_state, Unset):
            ui_state = UNSET
        elif isinstance(self.ui_state, ChatBotUiStateResponse):
            ui_state = self.ui_state.to_dict()
        else:
            ui_state = self.ui_state

        thread_ui_state: Union[Dict[str, Any], None, Unset]
        if isinstance(self.thread_ui_state, Unset):
            thread_ui_state = UNSET
        elif isinstance(self.thread_ui_state, ThreadUIState):
            thread_ui_state = self.thread_ui_state.to_dict()
        else:
            thread_ui_state = self.thread_ui_state

        chat_profile: Union[Dict[str, Any], None, Unset]
        if isinstance(self.chat_profile, Unset):
            chat_profile = UNSET
        elif isinstance(self.chat_profile, ChatProfile):
            chat_profile = self.chat_profile.to_dict()
        else:
            chat_profile = self.chat_profile

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if thread_form is not UNSET:
            field_dict["thread_form"] = thread_form
        if ui_state is not UNSET:
            field_dict["uiState"] = ui_state
        if thread_ui_state is not UNSET:
            field_dict["thread_ui_state"] = thread_ui_state
        if chat_profile is not UNSET:
            field_dict["chat_profile"] = chat_profile

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.chat_bot_ui_state_response import ChatBotUiStateResponse
        from ..models.chat_profile import ChatProfile
        from ..models.thread_form import ThreadForm
        from ..models.thread_ui_state import ThreadUIState

        d = src_dict.copy()

        def _parse_thread_form(data: object) -> Union["ThreadForm", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                thread_form_type_0 = ThreadForm.from_dict(data)

                return thread_form_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ThreadForm", None, Unset], data)

        thread_form = _parse_thread_form(d.pop("thread_form", UNSET))

        def _parse_ui_state(data: object) -> Union["ChatBotUiStateResponse", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                ui_state_type_0 = ChatBotUiStateResponse.from_dict(data)

                return ui_state_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ChatBotUiStateResponse", None, Unset], data)

        ui_state = _parse_ui_state(d.pop("uiState", UNSET))

        def _parse_thread_ui_state(data: object) -> Union["ThreadUIState", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                thread_ui_state_type_0 = ThreadUIState.from_dict(data)

                return thread_ui_state_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ThreadUIState", None, Unset], data)

        thread_ui_state = _parse_thread_ui_state(d.pop("thread_ui_state", UNSET))

        def _parse_chat_profile(data: object) -> Union["ChatProfile", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                chat_profile_type_0 = ChatProfile.from_dict(data)

                return chat_profile_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ChatProfile", None, Unset], data)

        chat_profile = _parse_chat_profile(d.pop("chat_profile", UNSET))

        types_response = cls(
            thread_form=thread_form,
            ui_state=ui_state,
            thread_ui_state=thread_ui_state,
            chat_profile=chat_profile,
        )

        types_response.additional_properties = d
        return types_response

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
