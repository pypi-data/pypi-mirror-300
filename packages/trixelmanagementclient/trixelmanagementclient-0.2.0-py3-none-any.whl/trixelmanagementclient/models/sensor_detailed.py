from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.measurement_type_enum import MeasurementTypeEnum
from typing import Dict
from typing import cast

if TYPE_CHECKING:
  from ..models.sensor_details import SensorDetails





T = TypeVar("T", bound="SensorDetailed")


@_attrs_define
class SensorDetailed:
    """ Sensor schema which also contains details.

        Attributes:
            measurement_station_uuid (str):
            id (int):
            measurement_type (MeasurementTypeEnum): Supported measurement types.
            details (SensorDetails): Schema for describing properties of sensors.
     """

    measurement_station_uuid: str
    id: int
    measurement_type: MeasurementTypeEnum
    details: 'SensorDetails'
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.sensor_details import SensorDetails
        measurement_station_uuid = self.measurement_station_uuid

        id = self.id

        measurement_type = self.measurement_type.value

        details = self.details.to_dict()


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "measurement_station_uuid": measurement_station_uuid,
            "id": id,
            "measurement_type": measurement_type,
            "details": details,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.sensor_details import SensorDetails
        d = src_dict.copy()
        measurement_station_uuid = d.pop("measurement_station_uuid")

        id = d.pop("id")

        measurement_type = MeasurementTypeEnum(d.pop("measurement_type"))




        details = SensorDetails.from_dict(d.pop("details"))




        sensor_detailed = cls(
            measurement_station_uuid=measurement_station_uuid,
            id=id,
            measurement_type=measurement_type,
            details=details,
        )


        sensor_detailed.additional_properties = d
        return sensor_detailed

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
