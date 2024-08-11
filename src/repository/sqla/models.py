import datetime

from sqlalchemy import MetaData, DateTime, Integer, JSON, Float, String
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


metadata = MetaData()


class Base(DeclarativeBase):
    metadata = metadata


class Battles(Base):
    __tablename__ = "battles"
    __table_args__ = {"schema": "ao"}

    bid: Mapped[int] = mapped_column(Integer, primary_key=True)
    starttime: Mapped[datetime] = mapped_column(DateTime)
    endtime: Mapped[datetime] = mapped_column(DateTime)
    timeout: Mapped[datetime] = mapped_column(DateTime)
    totalfame: Mapped[int] = mapped_column(Integer)
    totalkills: Mapped[int] = mapped_column(Integer)
    ao_battle_id: Mapped[int] = mapped_column(Integer)
    guild_member: Mapped[int] = mapped_column(Integer)
    total_member: Mapped[int] = mapped_column(Integer)
    guilds: Mapped[dict] = mapped_column(JSON)
    alliances: Mapped[dict] = mapped_column(JSON)


class PlayersBattle(Base):
    __tablename__ = "players_battle"
    __table_args__ = {"schema": "ao"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ip: Mapped[float] = mapped_column(Float)
    bid: Mapped[int] = mapped_column(Integer, nullable=False)
    kill: Mapped[int] = mapped_column(Integer, nullable=False)
    deaths: Mapped[int] = mapped_column(Integer, nullable=False)
    killfame: Mapped[int] = mapped_column(Integer, nullable=False)
    nickname: Mapped[str] = mapped_column(String(225), nullable=False)
    guildname: Mapped[str] = mapped_column(String(225), nullable=False)
    alliancename: Mapped[str] = mapped_column(String(225), nullable=False)
    mainhand: Mapped[str] = mapped_column(String(225))
