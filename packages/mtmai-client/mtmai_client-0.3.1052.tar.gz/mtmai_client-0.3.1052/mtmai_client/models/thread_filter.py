from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.thread_filter_feedback_type_0 import ThreadFilterFeedbackType0
from ..types import UNSET, Unset

T = TypeVar("T", bound="ThreadFilter")


@_attrs_define
class ThreadFilter:
    """
    Attributes:
        feedback (Union[None, ThreadFilterFeedbackType0, Unset]):
        user_id (Union[None, Unset, str]):
        search (Union[None, Unset, str]):
    """

    feedback: Union[None, ThreadFilterFeedbackType0, Unset] = UNSET
    user_id: Union[None, Unset, str] = UNSET
    search: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        feedback: Union[None, Unset, int]
        if isinstance(self.feedback, Unset):
            feedback = UNSET
        elif isinstance(self.feedback, ThreadFilterFeedbackType0):
            feedback = self.feedback.value
        else:
            feedback = self.feedback

        user_id: Union[None, Unset, str]
        if isinstance(self.user_id, Unset):
            user_id = UNSET
        else:
            user_id = self.user_id

        search: Union[None, Unset, str]
        if isinstance(self.search, Unset):
            search = UNSET
        else:
            search = self.search

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if feedback is not UNSET:
            field_dict["feedback"] = feedback
        if user_id is not UNSET:
            field_dict["userId"] = user_id
        if search is not UNSET:
            field_dict["search"] = search

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_feedback(data: object) -> Union[None, ThreadFilterFeedbackType0, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, int):
                    raise TypeError()
                feedback_type_0 = ThreadFilterFeedbackType0(data)

                return feedback_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, ThreadFilterFeedbackType0, Unset], data)

        feedback = _parse_feedback(d.pop("feedback", UNSET))

        def _parse_user_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_id = _parse_user_id(d.pop("userId", UNSET))

        def _parse_search(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        search = _parse_search(d.pop("search", UNSET))

        thread_filter = cls(
            feedback=feedback,
            user_id=user_id,
            search=search,
        )

        thread_filter.additional_properties = d
        return thread_filter

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
