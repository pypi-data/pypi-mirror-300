from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast, Union
from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="Measurement")


@_attrs_define
class Measurement:
    """ Schema which describes a single measurement performed by sensor within a measurement station.

        Attributes:
            timestamp (Union[datetime.datetime, int]): Point in time at which the measurement was taken (unix time).
            sensor_id (int): The ID of the sensor which took the measurement.
            value (Union[None, float]): The updated measurement value.
     """

    timestamp: Union[datetime.datetime, int]
    sensor_id: int
    value: Union[None, float]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        timestamp: Union[int, str]
        if isinstance(self.timestamp, datetime.datetime):
            timestamp = self.timestamp.isoformat()
        else:
            timestamp = self.timestamp

        sensor_id = self.sensor_id

        value: Union[None, float]
        value = self.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "timestamp": timestamp,
            "sensor_id": sensor_id,
            "value": value,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        def _parse_timestamp(data: object) -> Union[datetime.datetime, int]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                timestamp_type_0 = isoparse(data)



                return timestamp_type_0
            except: # noqa: E722
                pass
            return cast(Union[datetime.datetime, int], data)

        timestamp = _parse_timestamp(d.pop("timestamp"))


        sensor_id = d.pop("sensor_id")

        def _parse_value(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        value = _parse_value(d.pop("value"))


        measurement = cls(
            timestamp=timestamp,
            sensor_id=sensor_id,
            value=value,
        )


        measurement.additional_properties = d
        return measurement

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
