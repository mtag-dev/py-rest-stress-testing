from typing import List, Optional, Union
from dataclasses import dataclass, field

## - - - - - - -
## userinfo.json
## - - - - - - -


@dataclass
class UserAddress:
    formatted: str = ""


@dataclass
class UserInfoResponse:
    group_ids: List[str] = field(default_factory=list)
    sub: str = ""
    given_name: str = ""
    name: str = ""
    email: str = ""
    phone_number: Optional[str] = None
    address: Optional[UserAddress] = None
    picture: Optional[str] = None


## - - - - - - -
## sprint.json
## - - - - - - -

@dataclass
class Sprint:
    id: str
    name: str
    start: str
    end: str


@dataclass
class ShortUserInfo:
    id: str
    name: str
    picture: str


@dataclass
class Issue:
    id: str
    summary: str
    description_short: str
    index: int
    status_id: str
    story_points: int
    assigned: Optional[ShortUserInfo]
    modified_at: str


@dataclass
class SprintResponse:
    sprint: Sprint
    issues: List[Issue]


## - - - - - - -
## create-task.json
## - - - - - - -
@dataclass
class CreateTaskRequestBody:
    author: str
    assigned: str
    summary: str
    project: str
    sprint: str
    sprint: str
    labels: List[str]
    issue_type: str
    components: List[str]
    description: str
    priority: str


@dataclass
class CreateTaskPerson:
    id: str
    email: str
    name: str
    picture: str
    is_active: bool


@dataclass
class CreateTaskProject:
    id: str
    name: str


@dataclass
class CreateTaskStatus:
    id: str
    name: str


@dataclass
class CreateTaskActivity:
    user_id: str
    action: str
    created_at: str
    details: Union[CreateTaskPerson, CreateTaskStatus] = None


@dataclass
class CreateTaskResponse:
    author: CreateTaskPerson
    assigned: CreateTaskPerson
    summary: str
    project: CreateTaskProject
    sprint: str
    labels: List[str]
    issue_type: str
    components: List[str]
    description: str
    priority: str
    status: CreateTaskStatus
    activity: List[CreateTaskActivity]
    created_at: str
    modified_at: str
