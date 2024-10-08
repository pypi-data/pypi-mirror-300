from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.pagination import Pagination
    from ..models.thread_filter import ThreadFilter


T = TypeVar("T", bound="GetThreadsRequest")


@_attrs_define
class GetThreadsRequest:
    """
    Attributes:
        pagination (Pagination):
        filter_ (ThreadFilter):
    """

    pagination: "Pagination"
    filter_: "ThreadFilter"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pagination = self.pagination.to_dict()

        filter_ = self.filter_.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pagination": pagination,
                "filter": filter_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.pagination import Pagination
        from ..models.thread_filter import ThreadFilter

        d = src_dict.copy()
        pagination = Pagination.from_dict(d.pop("pagination"))

        filter_ = ThreadFilter.from_dict(d.pop("filter"))

        get_threads_request = cls(
            pagination=pagination,
            filter_=filter_,
        )

        get_threads_request.additional_properties = d
        return get_threads_request

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
