from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AccessTokenRepresentsAnAPIAccessToken")


@_attrs_define
class AccessTokenRepresentsAnAPIAccessToken:
    """
    Attributes:
        id (Union[Unset, int]):
        name (Union[Unset, str]):
        scopes (Union[Unset, List[str]]):
        sha1 (Union[Unset, str]):
        token_last_eight (Union[Unset, str]):
    """

    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    scopes: Union[Unset, List[str]] = UNSET
    sha1: Union[Unset, str] = UNSET
    token_last_eight: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        scopes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = self.scopes

        sha1 = self.sha1

        token_last_eight = self.token_last_eight

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if scopes is not UNSET:
            field_dict["scopes"] = scopes
        if sha1 is not UNSET:
            field_dict["sha1"] = sha1
        if token_last_eight is not UNSET:
            field_dict["token_last_eight"] = token_last_eight

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        scopes = cast(List[str], d.pop("scopes", UNSET))

        sha1 = d.pop("sha1", UNSET)

        token_last_eight = d.pop("token_last_eight", UNSET)

        access_token_represents_an_api_access_token = cls(
            id=id,
            name=name,
            scopes=scopes,
            sha1=sha1,
            token_last_eight=token_last_eight,
        )

        access_token_represents_an_api_access_token.additional_properties = d
        return access_token_represents_an_api_access_token

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
