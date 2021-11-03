from typing import List, Optional
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
