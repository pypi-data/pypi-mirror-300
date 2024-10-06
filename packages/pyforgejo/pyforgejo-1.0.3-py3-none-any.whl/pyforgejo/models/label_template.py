from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LabelTemplate")


@_attrs_define
class LabelTemplate:
    """LabelTemplate info of a Label template

    Attributes:
        color (Union[Unset, str]):  Example: 00aabb.
        description (Union[Unset, str]):
        exclusive (Union[Unset, bool]):
        name (Union[Unset, str]):
    """

    color: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    exclusive: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        color = self.color

        description = self.description

        exclusive = self.exclusive

        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if color is not UNSET:
            field_dict["color"] = color
        if description is not UNSET:
            field_dict["description"] = description
        if exclusive is not UNSET:
            field_dict["exclusive"] = exclusive
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        color = d.pop("color", UNSET)

        description = d.pop("description", UNSET)

        exclusive = d.pop("exclusive", UNSET)

        name = d.pop("name", UNSET)

        label_template = cls(
            color=color,
            description=description,
            exclusive=exclusive,
            name=name,
        )

        label_template.additional_properties = d
        return label_template

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
