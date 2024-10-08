from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.thread_form_display import ThreadFormDisplay
from ..models.thread_form_variant import ThreadFormVariant
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.input_widget_base import InputWidgetBase


T = TypeVar("T", bound="ThreadForm")


@_attrs_define
class ThreadForm:
    """发送Html 表单 向用户询问要执行任务的相关参数

    Attributes:
        inputs (List['InputWidgetBase']):
        open_ (Union[Unset, bool]):  Default: True.
        title (Union[Unset, str]):  Default: ''.
        description (Union[Unset, str]):  Default: ''.
        disable_submit_button (Union[Unset, bool]):  Default: False.
        display (Union[Unset, ThreadFormDisplay]):  Default: ThreadFormDisplay.MODAL.
        variant (Union[Unset, ThreadFormVariant]):  Default: ThreadFormVariant.DEFAULT.
    """

    inputs: List["InputWidgetBase"]
    open_: Union[Unset, bool] = True
    title: Union[Unset, str] = ""
    description: Union[Unset, str] = ""
    disable_submit_button: Union[Unset, bool] = False
    display: Union[Unset, ThreadFormDisplay] = ThreadFormDisplay.MODAL
    variant: Union[Unset, ThreadFormVariant] = ThreadFormVariant.DEFAULT
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        inputs = []
        for inputs_item_data in self.inputs:
            inputs_item = inputs_item_data.to_dict()
            inputs.append(inputs_item)

        open_ = self.open_

        title = self.title

        description = self.description

        disable_submit_button = self.disable_submit_button

        display: Union[Unset, str] = UNSET
        if not isinstance(self.display, Unset):
            display = self.display.value

        variant: Union[Unset, str] = UNSET
        if not isinstance(self.variant, Unset):
            variant = self.variant.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inputs": inputs,
            }
        )
        if open_ is not UNSET:
            field_dict["open"] = open_
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if disable_submit_button is not UNSET:
            field_dict["disable_submit_button"] = disable_submit_button
        if display is not UNSET:
            field_dict["display"] = display
        if variant is not UNSET:
            field_dict["variant"] = variant

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.input_widget_base import InputWidgetBase

        d = src_dict.copy()
        inputs = []
        _inputs = d.pop("inputs")
        for inputs_item_data in _inputs:
            inputs_item = InputWidgetBase.from_dict(inputs_item_data)

            inputs.append(inputs_item)

        open_ = d.pop("open", UNSET)

        title = d.pop("title", UNSET)

        description = d.pop("description", UNSET)

        disable_submit_button = d.pop("disable_submit_button", UNSET)

        _display = d.pop("display", UNSET)
        display: Union[Unset, ThreadFormDisplay]
        if isinstance(_display, Unset):
            display = UNSET
        else:
            display = ThreadFormDisplay(_display)

        _variant = d.pop("variant", UNSET)
        variant: Union[Unset, ThreadFormVariant]
        if isinstance(_variant, Unset):
            variant = UNSET
        else:
            variant = ThreadFormVariant(_variant)

        thread_form = cls(
            inputs=inputs,
            open_=open_,
            title=title,
            description=description,
            disable_submit_button=disable_submit_button,
            display=display,
            variant=variant,
        )

        thread_form.additional_properties = d
        return thread_form

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
