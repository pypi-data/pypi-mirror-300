from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.measurement_type_enum import MeasurementTypeEnum
from typing import cast, Union






T = TypeVar("T", bound="Observation")


@_attrs_define
class Observation:
    """ Schema which describes a single observation (at a point in time) for trixel&type.

        Attributes:
            time (int):
            trixel_id (int): A valid Trixel ID.
            measurement_type (MeasurementTypeEnum): Supported measurement types.
            value (Union[None, float]):
            sensor_count (int):
            measurement_station_count (int):
     """

    time: int
    trixel_id: int
    measurement_type: MeasurementTypeEnum
    value: Union[None, float]
    sensor_count: int
    measurement_station_count: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        time = self.time

        trixel_id = self.trixel_id

        measurement_type = self.measurement_type.value

        value: Union[None, float]
        value = self.value

        sensor_count = self.sensor_count

        measurement_station_count = self.measurement_station_count


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "time": time,
            "trixel_id": trixel_id,
            "measurement_type": measurement_type,
            "value": value,
            "sensor_count": sensor_count,
            "measurement_station_count": measurement_station_count,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        time = d.pop("time")

        trixel_id = d.pop("trixel_id")

        measurement_type = MeasurementTypeEnum(d.pop("measurement_type"))




        def _parse_value(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        value = _parse_value(d.pop("value"))


        sensor_count = d.pop("sensor_count")

        measurement_station_count = d.pop("measurement_station_count")

        observation = cls(
            time=time,
            trixel_id=trixel_id,
            measurement_type=measurement_type,
            value=value,
            sensor_count=sensor_count,
            measurement_station_count=measurement_station_count,
        )


        observation.additional_properties = d
        return observation

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
