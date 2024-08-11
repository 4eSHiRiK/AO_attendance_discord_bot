from abc import abstractmethod, ABC
from datetime import datetime

from src.interfaces.services.dto import (
    UserAttendanceOutputDTO,
    UserInfoOutputDTO,
    InactiveUserDTO,
)


class PlayersBattleRepositoryABC(ABC):

    @abstractmethod
    async def get_player_battle(self, name: str) -> UserInfoOutputDTO | None: ...

    @abstractmethod
    async def truncate_to_start_of_day(self, dt: datetime) -> datetime: ...

    @abstractmethod
    async def truncate_to_end_of_day(self, dt: datetime) -> datetime: ...

    @abstractmethod
    async def get_player_attendance(
        self, name: str, days: int
    ) -> UserAttendanceOutputDTO: ...

    @abstractmethod
    async def get_inactive_users(
        self, days: int, activity_threshold: int, percentage_threshold: int | None
    ) -> list[InactiveUserDTO] | None: ...
