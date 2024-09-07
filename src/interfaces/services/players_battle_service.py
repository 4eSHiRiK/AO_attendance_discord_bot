from abc import ABC, abstractmethod
from typing import Any

from src.interfaces.services.dto import (
    UserInfoOutputDTO,
    UserAttendanceOutputDTO,
    InactiveUserDTO,
)


class PlayersBattleServiceABC(ABC):
    @abstractmethod
    async def get_player_battle(self, name: str) -> UserInfoOutputDTO | None: ...

    @abstractmethod
    async def get_player_attendance(
        self, name: str, days: int
    ) -> UserAttendanceOutputDTO: ...

    @abstractmethod
    async def need_g_kick(
        self, days: int, activity_threshold: int, percentage_threshold: int | None
    ) -> list[InactiveUserDTO] | None: ...

    @abstractmethod
    async def fetch_guild_members(self) -> dict[str, Any]: ...
