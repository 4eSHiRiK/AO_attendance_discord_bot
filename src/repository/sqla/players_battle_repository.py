from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.interfaces.repositories.players_battle_repository import (
    PlayersBattleRepositoryABC,
)
from src.interfaces.services.dto import (
    UserAttendanceOutputDTO,
    UserInfoOutputDTO,
    InactiveUserDTO,
)
from src.repository.sqla.models import PlayersBattle, Battles
from datetime import datetime, timedelta
from sqlalchemy import func, and_


class PlayersBattleRepository(PlayersBattleRepositoryABC):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_player_battle(self, name: str) -> UserInfoOutputDTO:
        result = await self.session.execute(
            select(PlayersBattle).where(PlayersBattle.nickname == name)
        )
        player = result.scalars().first()
        return UserInfoOutputDTO(**player.__dict__)

    def truncate_to_start_of_day(self, dt: datetime) -> datetime:
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)

    def truncate_to_end_of_day(self, dt: datetime) -> datetime:
        return dt.replace(hour=23, minute=59, second=59, microsecond=999999)

    async def get_player_attendance(
        self, name: str, days: int
    ) -> UserAttendanceOutputDTO:
        end_date = self.truncate_to_end_of_day(datetime.utcnow())
        start_date = self.truncate_to_start_of_day(end_date - timedelta(days=days))

        stmt = (
            select(
                func.count().label("battle_count"),
                func.sum(PlayersBattle.kill).label("kills"),
                func.sum(PlayersBattle.deaths).label("deaths"),
            )
            .where(PlayersBattle.nickname == name)
            .where(
                PlayersBattle.bid.in_(
                    select(Battles.bid).where(
                        and_(
                            Battles.starttime.between(start_date, end_date),
                            Battles.guild_member > 30,
                        )
                    )
                )
            )
        )

        result = await self.session.execute(stmt)
        data = result.one()
        battle_count = data.battle_count or 0
        kills = data.kills or 0
        deaths = data.deaths or 1

        kd = round(kills / deaths, 1)

        stmt = (
            select(func.count().label("total_battle_count"))
            .select_from(Battles)
            .where(
                and_(
                    Battles.starttime.between(start_date, end_date),
                    Battles.guild_member > 30,
                )
            )
        )

        result = await self.session.execute(stmt)
        total_battle_count = result.scalar()
        percent_of_max = round((battle_count / total_battle_count) * 100, 1)

        return UserAttendanceOutputDTO(
            battle_count=battle_count, kd=kd, percent_of_max=percent_of_max
        )

    async def get_inactive_users(
        self, days: int, activity_threshold: int, percentage_threshold: int | None
    ) -> list[InactiveUserDTO] | None:
        end_date = self.truncate_to_end_of_day(datetime.utcnow())
        start_date = self.truncate_to_start_of_day(end_date - timedelta(days=days))
        threshold_date = self.truncate_to_start_of_day(
            datetime.utcnow() - timedelta(days=activity_threshold)
        )

        if percentage_threshold is None:
            percentage_threshold = 20

        stmt_max = (
            select(func.count().label("total_battle_count"))
            .select_from(Battles)
            .where(
                and_(
                    Battles.starttime.between(start_date, end_date),
                    Battles.guild_member > 30,
                )
            )
        )
        result_max = await self.session.execute(stmt_max)
        max_battle_count = result_max.scalar() or 1

        percentage_threshold_value = (percentage_threshold / 100) * max_battle_count

        stmt = (
            select(
                PlayersBattle.nickname,
                func.count().label("battle_count"),
                func.max(Battles.starttime).label("last_activity"),
            )
            .join(Battles, PlayersBattle.bid == Battles.bid)
            .where(
                and_(
                    PlayersBattle.guildname == "Sex and Flex",
                    Battles.starttime.between(start_date, end_date),
                    Battles.guild_member > 30,
                )
            )
            .group_by(PlayersBattle.nickname)
            .having(func.count() < percentage_threshold_value)
        )

        result = await self.session.execute(stmt)
        data = result.fetchall()

        inactive_users = [
            InactiveUserDTO(
                nickname=row.nickname,
                last_activity=row.last_activity,
                battle_count=row.battle_count,
            )
            for row in data
            if row.last_activity < threshold_date
        ]

        return inactive_users
