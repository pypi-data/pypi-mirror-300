from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast, Union






T = TypeVar("T", bound="SensorDetails")


@_attrs_define
class SensorDetails:
    """ Schema for describing properties of sensors.

        Attributes:
            accuracy (Union[None, float]):
            sensor_name (Union[None, str]):
     """

    accuracy: Union[None, float]
    sensor_name: Union[None, str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        accuracy: Union[None, float]
        accuracy = self.accuracy

        sensor_name: Union[None, str]
        sensor_name = self.sensor_name


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "accuracy": accuracy,
            "sensor_name": sensor_name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        def _parse_accuracy(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        accuracy = _parse_accuracy(d.pop("accuracy"))


        def _parse_sensor_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        sensor_name = _parse_sensor_name(d.pop("sensor_name"))


        sensor_details = cls(
            accuracy=accuracy,
            sensor_name=sensor_name,
        )


        sensor_details.additional_properties = d
        return sensor_details

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
