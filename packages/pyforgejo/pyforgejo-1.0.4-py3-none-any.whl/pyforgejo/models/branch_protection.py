import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="BranchProtection")


@_attrs_define
class BranchProtection:
    """BranchProtection represents a branch protection for a repository

    Attributes:
        approvals_whitelist_teams (Union[Unset, List[str]]):
        approvals_whitelist_username (Union[Unset, List[str]]):
        block_on_official_review_requests (Union[Unset, bool]):
        block_on_outdated_branch (Union[Unset, bool]):
        block_on_rejected_reviews (Union[Unset, bool]):
        branch_name (Union[Unset, str]): Deprecated: true
        created_at (Union[Unset, datetime.datetime]):
        dismiss_stale_approvals (Union[Unset, bool]):
        enable_approvals_whitelist (Union[Unset, bool]):
        enable_merge_whitelist (Union[Unset, bool]):
        enable_push (Union[Unset, bool]):
        enable_push_whitelist (Union[Unset, bool]):
        enable_status_check (Union[Unset, bool]):
        merge_whitelist_teams (Union[Unset, List[str]]):
        merge_whitelist_usernames (Union[Unset, List[str]]):
        protected_file_patterns (Union[Unset, str]):
        push_whitelist_deploy_keys (Union[Unset, bool]):
        push_whitelist_teams (Union[Unset, List[str]]):
        push_whitelist_usernames (Union[Unset, List[str]]):
        require_signed_commits (Union[Unset, bool]):
        required_approvals (Union[Unset, int]):
        rule_name (Union[Unset, str]):
        status_check_contexts (Union[Unset, List[str]]):
        unprotected_file_patterns (Union[Unset, str]):
        updated_at (Union[Unset, datetime.datetime]):
    """

    approvals_whitelist_teams: Union[Unset, List[str]] = UNSET
    approvals_whitelist_username: Union[Unset, List[str]] = UNSET
    block_on_official_review_requests: Union[Unset, bool] = UNSET
    block_on_outdated_branch: Union[Unset, bool] = UNSET
    block_on_rejected_reviews: Union[Unset, bool] = UNSET
    branch_name: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    dismiss_stale_approvals: Union[Unset, bool] = UNSET
    enable_approvals_whitelist: Union[Unset, bool] = UNSET
    enable_merge_whitelist: Union[Unset, bool] = UNSET
    enable_push: Union[Unset, bool] = UNSET
    enable_push_whitelist: Union[Unset, bool] = UNSET
    enable_status_check: Union[Unset, bool] = UNSET
    merge_whitelist_teams: Union[Unset, List[str]] = UNSET
    merge_whitelist_usernames: Union[Unset, List[str]] = UNSET
    protected_file_patterns: Union[Unset, str] = UNSET
    push_whitelist_deploy_keys: Union[Unset, bool] = UNSET
    push_whitelist_teams: Union[Unset, List[str]] = UNSET
    push_whitelist_usernames: Union[Unset, List[str]] = UNSET
    require_signed_commits: Union[Unset, bool] = UNSET
    required_approvals: Union[Unset, int] = UNSET
    rule_name: Union[Unset, str] = UNSET
    status_check_contexts: Union[Unset, List[str]] = UNSET
    unprotected_file_patterns: Union[Unset, str] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        approvals_whitelist_teams: Union[Unset, List[str]] = UNSET
        if not isinstance(self.approvals_whitelist_teams, Unset):
            approvals_whitelist_teams = self.approvals_whitelist_teams

        approvals_whitelist_username: Union[Unset, List[str]] = UNSET
        if not isinstance(self.approvals_whitelist_username, Unset):
            approvals_whitelist_username = self.approvals_whitelist_username

        block_on_official_review_requests = self.block_on_official_review_requests

        block_on_outdated_branch = self.block_on_outdated_branch

        block_on_rejected_reviews = self.block_on_rejected_reviews

        branch_name = self.branch_name

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        dismiss_stale_approvals = self.dismiss_stale_approvals

        enable_approvals_whitelist = self.enable_approvals_whitelist

        enable_merge_whitelist = self.enable_merge_whitelist

        enable_push = self.enable_push

        enable_push_whitelist = self.enable_push_whitelist

        enable_status_check = self.enable_status_check

        merge_whitelist_teams: Union[Unset, List[str]] = UNSET
        if not isinstance(self.merge_whitelist_teams, Unset):
            merge_whitelist_teams = self.merge_whitelist_teams

        merge_whitelist_usernames: Union[Unset, List[str]] = UNSET
        if not isinstance(self.merge_whitelist_usernames, Unset):
            merge_whitelist_usernames = self.merge_whitelist_usernames

        protected_file_patterns = self.protected_file_patterns

        push_whitelist_deploy_keys = self.push_whitelist_deploy_keys

        push_whitelist_teams: Union[Unset, List[str]] = UNSET
        if not isinstance(self.push_whitelist_teams, Unset):
            push_whitelist_teams = self.push_whitelist_teams

        push_whitelist_usernames: Union[Unset, List[str]] = UNSET
        if not isinstance(self.push_whitelist_usernames, Unset):
            push_whitelist_usernames = self.push_whitelist_usernames

        require_signed_commits = self.require_signed_commits

        required_approvals = self.required_approvals

        rule_name = self.rule_name

        status_check_contexts: Union[Unset, List[str]] = UNSET
        if not isinstance(self.status_check_contexts, Unset):
            status_check_contexts = self.status_check_contexts

        unprotected_file_patterns = self.unprotected_file_patterns

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if approvals_whitelist_teams is not UNSET:
            field_dict["approvals_whitelist_teams"] = approvals_whitelist_teams
        if approvals_whitelist_username is not UNSET:
            field_dict["approvals_whitelist_username"] = approvals_whitelist_username
        if block_on_official_review_requests is not UNSET:
            field_dict["block_on_official_review_requests"] = block_on_official_review_requests
        if block_on_outdated_branch is not UNSET:
            field_dict["block_on_outdated_branch"] = block_on_outdated_branch
        if block_on_rejected_reviews is not UNSET:
            field_dict["block_on_rejected_reviews"] = block_on_rejected_reviews
        if branch_name is not UNSET:
            field_dict["branch_name"] = branch_name
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if dismiss_stale_approvals is not UNSET:
            field_dict["dismiss_stale_approvals"] = dismiss_stale_approvals
        if enable_approvals_whitelist is not UNSET:
            field_dict["enable_approvals_whitelist"] = enable_approvals_whitelist
        if enable_merge_whitelist is not UNSET:
            field_dict["enable_merge_whitelist"] = enable_merge_whitelist
        if enable_push is not UNSET:
            field_dict["enable_push"] = enable_push
        if enable_push_whitelist is not UNSET:
            field_dict["enable_push_whitelist"] = enable_push_whitelist
        if enable_status_check is not UNSET:
            field_dict["enable_status_check"] = enable_status_check
        if merge_whitelist_teams is not UNSET:
            field_dict["merge_whitelist_teams"] = merge_whitelist_teams
        if merge_whitelist_usernames is not UNSET:
            field_dict["merge_whitelist_usernames"] = merge_whitelist_usernames
        if protected_file_patterns is not UNSET:
            field_dict["protected_file_patterns"] = protected_file_patterns
        if push_whitelist_deploy_keys is not UNSET:
            field_dict["push_whitelist_deploy_keys"] = push_whitelist_deploy_keys
        if push_whitelist_teams is not UNSET:
            field_dict["push_whitelist_teams"] = push_whitelist_teams
        if push_whitelist_usernames is not UNSET:
            field_dict["push_whitelist_usernames"] = push_whitelist_usernames
        if require_signed_commits is not UNSET:
            field_dict["require_signed_commits"] = require_signed_commits
        if required_approvals is not UNSET:
            field_dict["required_approvals"] = required_approvals
        if rule_name is not UNSET:
            field_dict["rule_name"] = rule_name
        if status_check_contexts is not UNSET:
            field_dict["status_check_contexts"] = status_check_contexts
        if unprotected_file_patterns is not UNSET:
            field_dict["unprotected_file_patterns"] = unprotected_file_patterns
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        approvals_whitelist_teams = cast(List[str], d.pop("approvals_whitelist_teams", UNSET))

        approvals_whitelist_username = cast(List[str], d.pop("approvals_whitelist_username", UNSET))

        block_on_official_review_requests = d.pop("block_on_official_review_requests", UNSET)

        block_on_outdated_branch = d.pop("block_on_outdated_branch", UNSET)

        block_on_rejected_reviews = d.pop("block_on_rejected_reviews", UNSET)

        branch_name = d.pop("branch_name", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        dismiss_stale_approvals = d.pop("dismiss_stale_approvals", UNSET)

        enable_approvals_whitelist = d.pop("enable_approvals_whitelist", UNSET)

        enable_merge_whitelist = d.pop("enable_merge_whitelist", UNSET)

        enable_push = d.pop("enable_push", UNSET)

        enable_push_whitelist = d.pop("enable_push_whitelist", UNSET)

        enable_status_check = d.pop("enable_status_check", UNSET)

        merge_whitelist_teams = cast(List[str], d.pop("merge_whitelist_teams", UNSET))

        merge_whitelist_usernames = cast(List[str], d.pop("merge_whitelist_usernames", UNSET))

        protected_file_patterns = d.pop("protected_file_patterns", UNSET)

        push_whitelist_deploy_keys = d.pop("push_whitelist_deploy_keys", UNSET)

        push_whitelist_teams = cast(List[str], d.pop("push_whitelist_teams", UNSET))

        push_whitelist_usernames = cast(List[str], d.pop("push_whitelist_usernames", UNSET))

        require_signed_commits = d.pop("require_signed_commits", UNSET)

        required_approvals = d.pop("required_approvals", UNSET)

        rule_name = d.pop("rule_name", UNSET)

        status_check_contexts = cast(List[str], d.pop("status_check_contexts", UNSET))

        unprotected_file_patterns = d.pop("unprotected_file_patterns", UNSET)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        branch_protection = cls(
            approvals_whitelist_teams=approvals_whitelist_teams,
            approvals_whitelist_username=approvals_whitelist_username,
            block_on_official_review_requests=block_on_official_review_requests,
            block_on_outdated_branch=block_on_outdated_branch,
            block_on_rejected_reviews=block_on_rejected_reviews,
            branch_name=branch_name,
            created_at=created_at,
            dismiss_stale_approvals=dismiss_stale_approvals,
            enable_approvals_whitelist=enable_approvals_whitelist,
            enable_merge_whitelist=enable_merge_whitelist,
            enable_push=enable_push,
            enable_push_whitelist=enable_push_whitelist,
            enable_status_check=enable_status_check,
            merge_whitelist_teams=merge_whitelist_teams,
            merge_whitelist_usernames=merge_whitelist_usernames,
            protected_file_patterns=protected_file_patterns,
            push_whitelist_deploy_keys=push_whitelist_deploy_keys,
            push_whitelist_teams=push_whitelist_teams,
            push_whitelist_usernames=push_whitelist_usernames,
            require_signed_commits=require_signed_commits,
            required_approvals=required_approvals,
            rule_name=rule_name,
            status_check_contexts=status_check_contexts,
            unprotected_file_patterns=unprotected_file_patterns,
            updated_at=updated_at,
        )

        branch_protection.additional_properties = d
        return branch_protection

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
