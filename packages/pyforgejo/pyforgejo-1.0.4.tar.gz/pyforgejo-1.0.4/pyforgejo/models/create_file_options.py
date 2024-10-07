from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.commit_date_options import CommitDateOptions
    from ..models.identity import Identity


T = TypeVar("T", bound="CreateFileOptions")


@_attrs_define
class CreateFileOptions:
    """CreateFileOptions options for creating files
    Note: `author` and `committer` are optional (if only one is given, it will be used for the other, otherwise the
    authenticated user will be used)

        Attributes:
            content (str): content must be base64 encoded
            author (Union[Unset, Identity]): Identity for a person's identity like an author or committer
            branch (Union[Unset, str]): branch (optional) to base this file from. if not given, the default branch is used
            committer (Union[Unset, Identity]): Identity for a person's identity like an author or committer
            dates (Union[Unset, CommitDateOptions]): CommitDateOptions store dates for GIT_AUTHOR_DATE and
                GIT_COMMITTER_DATE
            message (Union[Unset, str]): message (optional) for the commit of this file. if not supplied, a default message
                will be used
            new_branch (Union[Unset, str]): new_branch (optional) will make a new branch from `branch` before creating the
                file
            signoff (Union[Unset, bool]): Add a Signed-off-by trailer by the committer at the end of the commit log message.
    """

    content: str
    author: Union[Unset, "Identity"] = UNSET
    branch: Union[Unset, str] = UNSET
    committer: Union[Unset, "Identity"] = UNSET
    dates: Union[Unset, "CommitDateOptions"] = UNSET
    message: Union[Unset, str] = UNSET
    new_branch: Union[Unset, str] = UNSET
    signoff: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        content = self.content

        author: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.author, Unset):
            author = self.author.to_dict()

        branch = self.branch

        committer: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.committer, Unset):
            committer = self.committer.to_dict()

        dates: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.dates, Unset):
            dates = self.dates.to_dict()

        message = self.message

        new_branch = self.new_branch

        signoff = self.signoff

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
            }
        )
        if author is not UNSET:
            field_dict["author"] = author
        if branch is not UNSET:
            field_dict["branch"] = branch
        if committer is not UNSET:
            field_dict["committer"] = committer
        if dates is not UNSET:
            field_dict["dates"] = dates
        if message is not UNSET:
            field_dict["message"] = message
        if new_branch is not UNSET:
            field_dict["new_branch"] = new_branch
        if signoff is not UNSET:
            field_dict["signoff"] = signoff

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.commit_date_options import CommitDateOptions
        from ..models.identity import Identity

        d = src_dict.copy()
        content = d.pop("content")

        _author = d.pop("author", UNSET)
        author: Union[Unset, Identity]
        if isinstance(_author, Unset):
            author = UNSET
        else:
            author = Identity.from_dict(_author)

        branch = d.pop("branch", UNSET)

        _committer = d.pop("committer", UNSET)
        committer: Union[Unset, Identity]
        if isinstance(_committer, Unset):
            committer = UNSET
        else:
            committer = Identity.from_dict(_committer)

        _dates = d.pop("dates", UNSET)
        dates: Union[Unset, CommitDateOptions]
        if isinstance(_dates, Unset):
            dates = UNSET
        else:
            dates = CommitDateOptions.from_dict(_dates)

        message = d.pop("message", UNSET)

        new_branch = d.pop("new_branch", UNSET)

        signoff = d.pop("signoff", UNSET)

        create_file_options = cls(
            content=content,
            author=author,
            branch=branch,
            committer=committer,
            dates=dates,
            message=message,
            new_branch=new_branch,
            signoff=signoff,
        )

        create_file_options.additional_properties = d
        return create_file_options

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
