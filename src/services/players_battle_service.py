from pydantic import TypeAdapter

from src.interfaces.repositories.players_battle_repository import (
    PlayersBattleRepositoryABC,
)
from src.interfaces.services.dto import (
    UserInfoOutputDTO,
    UserAttendanceOutputDTO,
    InactiveUserDTO,
)
from src.interfaces.services.players_battle_service import PlayersBattleServiceABC
from src.repository.sqla.db import database
from src.repository.sqla.players_battle_repository import PlayersBattleRepository


class PlayersBattleService(PlayersBattleServiceABC):

    async def get_player_battle(self, name: str) -> UserInfoOutputDTO | None:
        async with database.session_factory() as session:
            repository: PlayersBattleRepositoryABC = PlayersBattleRepository(session)
            player_battle = await repository.get_player_battle(name)

            if player_battle:
                return player_battle
            return None

    async def get_player_attendance(
        self, name: str, days: int
    ) -> UserAttendanceOutputDTO:
        async with database.session_factory() as session:
            repository: PlayersBattleRepositoryABC = PlayersBattleRepository(session)
            player_attendance = await repository.get_player_attendance(name, days)
            return player_attendance

    async def need_g_kick(
        self, days: int, activity_threshold: int, percentage_threshold: int | None
    ) -> list[InactiveUserDTO] | None:
        async with database.session_factory() as session:
            repository: PlayersBattleRepositoryABC = PlayersBattleRepository(session)
            player_list = await repository.get_inactive_users(
                days, activity_threshold, percentage_threshold
            )
            if player_list:
                return player_list
            return None
