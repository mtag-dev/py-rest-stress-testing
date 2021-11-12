from typing import List, Optional, Union
from pydantic import BaseModel, Field

## - - - - - - -
## userinfo.json
## - - - - - - -


class UserAddress(BaseModel):
    formatted: str = ""


class UserInfoResponse(BaseModel):
    group_ids: List[str] = Field(default_factory=list)
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

class Sprint(BaseModel):
    id: str
    name: str
    start: str
    end: str


class ShortUserInfo(BaseModel):
    id: str
    name: str
    picture: str


class Issue(BaseModel):
    id: str
    summary: str
    description_short: str
    index: int
    status_id: str
    story_points: int
    assigned: Optional[ShortUserInfo]
    modified_at: str


class SprintResponse(BaseModel):
    sprint: Sprint
    issues: List[Issue]


## - - - - - - -
## create-task.json
## - - - - - - -

class CreateTaskRequestBody(BaseModel):
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


class CreateTaskPerson(BaseModel):
    id: str
    email: str
    name: str
    picture: str
    is_active: bool


class CreateTaskProject(BaseModel):
    id: str
    name: str


class CreateTaskStatus(BaseModel):
    id: str
    name: str


class CreateTaskActivity(BaseModel):
    user_id: str
    action: str
    created_at: str
    details: Union[CreateTaskPerson, CreateTaskStatus] = None


class CreateTaskResponse(BaseModel):
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
