from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chat_messages_item_artifacts_type_0_item import ChatMessagesItemArtifactsType0Item
    from ..models.chat_messages_item_props_type_0 import ChatMessagesItemPropsType0


T = TypeVar("T", bound="ChatMessagesItem")


@_attrs_define
class ChatMessagesItem:
    """
    Attributes:
        id (str):
        role (Union[None, Unset, str]):
        content (Union[None, Unset, str]):
        component (Union[None, Unset, str]):
        props (Union['ChatMessagesItemPropsType0', None, Unset]):
        artifacts (Union[List['ChatMessagesItemArtifactsType0Item'], None, Unset]):
    """

    id: str
    role: Union[None, Unset, str] = UNSET
    content: Union[None, Unset, str] = UNSET
    component: Union[None, Unset, str] = UNSET
    props: Union["ChatMessagesItemPropsType0", None, Unset] = UNSET
    artifacts: Union[List["ChatMessagesItemArtifactsType0Item"], None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.chat_messages_item_props_type_0 import ChatMessagesItemPropsType0

        id = self.id

        role: Union[None, Unset, str]
        if isinstance(self.role, Unset):
            role = UNSET
        else:
            role = self.role

        content: Union[None, Unset, str]
        if isinstance(self.content, Unset):
            content = UNSET
        else:
            content = self.content

        component: Union[None, Unset, str]
        if isinstance(self.component, Unset):
            component = UNSET
        else:
            component = self.component

        props: Union[Dict[str, Any], None, Unset]
        if isinstance(self.props, Unset):
            props = UNSET
        elif isinstance(self.props, ChatMessagesItemPropsType0):
            props = self.props.to_dict()
        else:
            props = self.props

        artifacts: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.artifacts, Unset):
            artifacts = UNSET
        elif isinstance(self.artifacts, list):
            artifacts = []
            for artifacts_type_0_item_data in self.artifacts:
                artifacts_type_0_item = artifacts_type_0_item_data.to_dict()
                artifacts.append(artifacts_type_0_item)

        else:
            artifacts = self.artifacts

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if role is not UNSET:
            field_dict["role"] = role
        if content is not UNSET:
            field_dict["content"] = content
        if component is not UNSET:
            field_dict["component"] = component
        if props is not UNSET:
            field_dict["props"] = props
        if artifacts is not UNSET:
            field_dict["artifacts"] = artifacts

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.chat_messages_item_artifacts_type_0_item import ChatMessagesItemArtifactsType0Item
        from ..models.chat_messages_item_props_type_0 import ChatMessagesItemPropsType0

        d = src_dict.copy()
        id = d.pop("id")

        def _parse_role(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        role = _parse_role(d.pop("role", UNSET))

        def _parse_content(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        content = _parse_content(d.pop("content", UNSET))

        def _parse_component(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        component = _parse_component(d.pop("component", UNSET))

        def _parse_props(data: object) -> Union["ChatMessagesItemPropsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                props_type_0 = ChatMessagesItemPropsType0.from_dict(data)

                return props_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ChatMessagesItemPropsType0", None, Unset], data)

        props = _parse_props(d.pop("props", UNSET))

        def _parse_artifacts(data: object) -> Union[List["ChatMessagesItemArtifactsType0Item"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                artifacts_type_0 = []
                _artifacts_type_0 = data
                for artifacts_type_0_item_data in _artifacts_type_0:
                    artifacts_type_0_item = ChatMessagesItemArtifactsType0Item.from_dict(artifacts_type_0_item_data)

                    artifacts_type_0.append(artifacts_type_0_item)

                return artifacts_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["ChatMessagesItemArtifactsType0Item"], None, Unset], data)

        artifacts = _parse_artifacts(d.pop("artifacts", UNSET))

        chat_messages_item = cls(
            id=id,
            role=role,
            content=content,
            component=component,
            props=props,
            artifacts=artifacts,
        )

        chat_messages_item.additional_properties = d
        return chat_messages_item

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
