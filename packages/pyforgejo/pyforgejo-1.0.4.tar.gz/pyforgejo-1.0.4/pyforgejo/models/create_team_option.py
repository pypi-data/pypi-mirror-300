from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_team_option_permission import CreateTeamOptionPermission
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_team_option_units_map import CreateTeamOptionUnitsMap


T = TypeVar("T", bound="CreateTeamOption")


@_attrs_define
class CreateTeamOption:
    """CreateTeamOption options for creating a team

    Attributes:
        name (str):
        can_create_org_repo (Union[Unset, bool]):
        description (Union[Unset, str]):
        includes_all_repositories (Union[Unset, bool]):
        permission (Union[Unset, CreateTeamOptionPermission]):
        units (Union[Unset, List[str]]):  Example: ['repo.actions', 'repo.code', 'repo.issues', 'repo.ext_issues',
            'repo.wiki', 'repo.ext_wiki', 'repo.pulls', 'repo.releases', 'repo.projects', 'repo.ext_wiki'].
        units_map (Union[Unset, CreateTeamOptionUnitsMap]):  Example: {"repo.actions","repo.packages","repo.code":"read"
            ,"repo.issues":"write","repo.ext_issues":"none","repo.wiki":"admin","repo.pulls":"owner","repo.releases":"none",
            "repo.projects":"none","repo.ext_wiki":"none"}.
    """

    name: str
    can_create_org_repo: Union[Unset, bool] = UNSET
    description: Union[Unset, str] = UNSET
    includes_all_repositories: Union[Unset, bool] = UNSET
    permission: Union[Unset, CreateTeamOptionPermission] = UNSET
    units: Union[Unset, List[str]] = UNSET
    units_map: Union[Unset, "CreateTeamOptionUnitsMap"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        can_create_org_repo = self.can_create_org_repo

        description = self.description

        includes_all_repositories = self.includes_all_repositories

        permission: Union[Unset, str] = UNSET
        if not isinstance(self.permission, Unset):
            permission = self.permission.value

        units: Union[Unset, List[str]] = UNSET
        if not isinstance(self.units, Unset):
            units = self.units

        units_map: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.units_map, Unset):
            units_map = self.units_map.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if can_create_org_repo is not UNSET:
            field_dict["can_create_org_repo"] = can_create_org_repo
        if description is not UNSET:
            field_dict["description"] = description
        if includes_all_repositories is not UNSET:
            field_dict["includes_all_repositories"] = includes_all_repositories
        if permission is not UNSET:
            field_dict["permission"] = permission
        if units is not UNSET:
            field_dict["units"] = units
        if units_map is not UNSET:
            field_dict["units_map"] = units_map

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_team_option_units_map import CreateTeamOptionUnitsMap

        d = src_dict.copy()
        name = d.pop("name")

        can_create_org_repo = d.pop("can_create_org_repo", UNSET)

        description = d.pop("description", UNSET)

        includes_all_repositories = d.pop("includes_all_repositories", UNSET)

        _permission = d.pop("permission", UNSET)
        permission: Union[Unset, CreateTeamOptionPermission]
        if isinstance(_permission, Unset):
            permission = UNSET
        else:
            permission = CreateTeamOptionPermission(_permission)

        units = cast(List[str], d.pop("units", UNSET))

        _units_map = d.pop("units_map", UNSET)
        units_map: Union[Unset, CreateTeamOptionUnitsMap]
        if isinstance(_units_map, Unset):
            units_map = UNSET
        else:
            units_map = CreateTeamOptionUnitsMap.from_dict(_units_map)

        create_team_option = cls(
            name=name,
            can_create_org_repo=can_create_org_repo,
            description=description,
            includes_all_repositories=includes_all_repositories,
            permission=permission,
            units=units,
            units_map=units_map,
        )

        create_team_option.additional_properties = d
        return create_team_option

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
