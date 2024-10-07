from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="MeasurementStation")


@_attrs_define
class MeasurementStation:
    """ Schema for generic queries related to measurement stations.

        Attributes:
            uuid (str):
            active (bool):
            k_requirement (int):
     """

    uuid: str
    active: bool
    k_requirement: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        uuid = self.uuid

        active = self.active

        k_requirement = self.k_requirement


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "uuid": uuid,
            "active": active,
            "k_requirement": k_requirement,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        uuid = d.pop("uuid")

        active = d.pop("active")

        k_requirement = d.pop("k_requirement")

        measurement_station = cls(
            uuid=uuid,
            active=active,
            k_requirement=k_requirement,
        )


        measurement_station.additional_properties = d
        return measurement_station

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
