from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.issue_form_field_validations_additional_property import IssueFormFieldValidationsAdditionalProperty


T = TypeVar("T", bound="IssueFormFieldValidations")


@_attrs_define
class IssueFormFieldValidations:
    """ """

    additional_properties: Dict[str, "IssueFormFieldValidationsAdditionalProperty"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.issue_form_field_validations_additional_property import (
            IssueFormFieldValidationsAdditionalProperty,
        )

        d = src_dict.copy()
        issue_form_field_validations = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = IssueFormFieldValidationsAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        issue_form_field_validations.additional_properties = additional_properties
        return issue_form_field_validations

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "IssueFormFieldValidationsAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "IssueFormFieldValidationsAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
