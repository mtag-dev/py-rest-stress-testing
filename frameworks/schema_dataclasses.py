from typing import List, Optional
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
