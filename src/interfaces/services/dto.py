from datetime import datetime
from typing import Any

from pydantic import BaseModel


class UserInfoOutputDTO(BaseModel):
    nickname: str
    guildname: str
    alliancename: str


class UserAttendanceOutputDTO(BaseModel):
    battle_count: int
    kd: float
    percent_of_max: Any


class InactiveUserDTO(BaseModel):
    nickname: str
    last_activity: datetime
    battle_count: int
