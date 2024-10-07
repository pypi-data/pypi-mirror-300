from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast, List
from typing import Dict
from typing import cast

if TYPE_CHECKING:
  from ..models.measurement import Measurement





T = TypeVar("T", bound="PublishSensorUpdatesToTrixelsTrixelUpdatePutUpdates")


@_attrs_define
class PublishSensorUpdatesToTrixelsTrixelUpdatePutUpdates:
    """ A dictionary where for each trixel, sensors with their updated measurements are described.

     """

    additional_properties: Dict[str, List['Measurement']] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.measurement import Measurement
        
        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = []
            for additional_property_item_data in prop:
                additional_property_item = additional_property_item_data.to_dict()
                field_dict[prop_name].append(additional_property_item)



        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.measurement import Measurement
        d = src_dict.copy()
        publish_sensor_updates_to_trixels_trixel_update_put_updates = cls(
        )


        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = []
            _additional_property = prop_dict
            for additional_property_item_data in (_additional_property):
                additional_property_item = Measurement.from_dict(additional_property_item_data)



                additional_property.append(additional_property_item)

            additional_properties[prop_name] = additional_property

        publish_sensor_updates_to_trixels_trixel_update_put_updates.additional_properties = additional_properties
        return publish_sensor_updates_to_trixels_trixel_update_put_updates

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> List['Measurement']:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: List['Measurement']) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
