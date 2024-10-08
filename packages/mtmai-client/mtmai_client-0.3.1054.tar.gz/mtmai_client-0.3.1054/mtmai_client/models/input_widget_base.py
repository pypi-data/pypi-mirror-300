from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.input_widget_base_type_type_0 import InputWidgetBaseTypeType0
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.input_widget_base_items_item import InputWidgetBaseItemsItem
    from ..models.input_widget_base_options_type_0 import InputWidgetBaseOptionsType0


T = TypeVar("T", bound="InputWidgetBase")


@_attrs_define
class InputWidgetBase:
    """输入组件的基类, 对应全段标准 html input 组件

    Attributes:
        id (Union[None, Unset, str]):
        name (Union[None, Unset, str]):
        placeholder (Union[None, Unset, str]):
        label (Union[None, Unset, str]):
        tooltip (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        type (Union[InputWidgetBaseTypeType0, None, Unset]):  Default: InputWidgetBaseTypeType0.STRING.
        value (Union[None, Unset, str]):
        items (Union[Unset, List['InputWidgetBaseItemsItem']]):
        options (Union['InputWidgetBaseOptionsType0', None, Unset]):
    """

    id: Union[None, Unset, str] = UNSET
    name: Union[None, Unset, str] = UNSET
    placeholder: Union[None, Unset, str] = UNSET
    label: Union[None, Unset, str] = UNSET
    tooltip: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    type: Union[InputWidgetBaseTypeType0, None, Unset] = InputWidgetBaseTypeType0.STRING
    value: Union[None, Unset, str] = UNSET
    items: Union[Unset, List["InputWidgetBaseItemsItem"]] = UNSET
    options: Union["InputWidgetBaseOptionsType0", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.input_widget_base_options_type_0 import InputWidgetBaseOptionsType0

        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        placeholder: Union[None, Unset, str]
        if isinstance(self.placeholder, Unset):
            placeholder = UNSET
        else:
            placeholder = self.placeholder

        label: Union[None, Unset, str]
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        tooltip: Union[None, Unset, str]
        if isinstance(self.tooltip, Unset):
            tooltip = UNSET
        else:
            tooltip = self.tooltip

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        type: Union[None, Unset, str]
        if isinstance(self.type, Unset):
            type = UNSET
        elif isinstance(self.type, InputWidgetBaseTypeType0):
            type = self.type.value
        else:
            type = self.type

        value: Union[None, Unset, str]
        if isinstance(self.value, Unset):
            value = UNSET
        else:
            value = self.value

        items: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.items, Unset):
            items = []
            for items_item_data in self.items:
                items_item = items_item_data.to_dict()
                items.append(items_item)

        options: Union[Dict[str, Any], None, Unset]
        if isinstance(self.options, Unset):
            options = UNSET
        elif isinstance(self.options, InputWidgetBaseOptionsType0):
            options = self.options.to_dict()
        else:
            options = self.options

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if placeholder is not UNSET:
            field_dict["placeholder"] = placeholder
        if label is not UNSET:
            field_dict["label"] = label
        if tooltip is not UNSET:
            field_dict["tooltip"] = tooltip
        if description is not UNSET:
            field_dict["description"] = description
        if type is not UNSET:
            field_dict["type"] = type
        if value is not UNSET:
            field_dict["value"] = value
        if items is not UNSET:
            field_dict["items"] = items
        if options is not UNSET:
            field_dict["options"] = options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.input_widget_base_items_item import InputWidgetBaseItemsItem
        from ..models.input_widget_base_options_type_0 import InputWidgetBaseOptionsType0

        d = src_dict.copy()

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_placeholder(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        placeholder = _parse_placeholder(d.pop("placeholder", UNSET))

        def _parse_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_tooltip(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tooltip = _parse_tooltip(d.pop("tooltip", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_type(data: object) -> Union[InputWidgetBaseTypeType0, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                type_type_0 = InputWidgetBaseTypeType0(data)

                return type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[InputWidgetBaseTypeType0, None, Unset], data)

        type = _parse_type(d.pop("type", UNSET))

        def _parse_value(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        value = _parse_value(d.pop("value", UNSET))

        items = []
        _items = d.pop("items", UNSET)
        for items_item_data in _items or []:
            items_item = InputWidgetBaseItemsItem.from_dict(items_item_data)

            items.append(items_item)

        def _parse_options(data: object) -> Union["InputWidgetBaseOptionsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                options_type_0 = InputWidgetBaseOptionsType0.from_dict(data)

                return options_type_0
            except:  # noqa: E722
                pass
            return cast(Union["InputWidgetBaseOptionsType0", None, Unset], data)

        options = _parse_options(d.pop("options", UNSET))

        input_widget_base = cls(
            id=id,
            name=name,
            placeholder=placeholder,
            label=label,
            tooltip=tooltip,
            description=description,
            type=type,
            value=value,
            items=items,
            options=options,
        )

        input_widget_base.additional_properties = d
        return input_widget_base

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
