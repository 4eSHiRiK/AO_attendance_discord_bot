from collections.abc import Callable
from typing import Any

from pydantic.json import pydantic_encoder
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)
import orjson
from src.core.settings import (
    db_dsn,
    pool_size,
    max_overflow,
    pool_pre_ping,
    connection_timeout,
    command_timeout,
    app_name,
    timezone,
)


def orjson_dumps(
    value: Any, *, default: Callable[[Any], Any] = pydantic_encoder
) -> str:
    return orjson.dumps(value, default=default).decode()


class Database:
    def __init__(self) -> None:
        self._engine: AsyncEngine = create_async_engine(
            url=str(db_dsn),
            pool_size=int(pool_size),
            max_overflow=int(max_overflow),
            pool_pre_ping=pool_pre_ping,
            connect_args={
                "timeout": int(connection_timeout),
                "command_timeout": int(command_timeout),
                "server_settings": {
                    "jit": "off",
                    "application_name": str(app_name),
                    "timezone": str(timezone),
                },
            },
            json_serializer=orjson_dumps,
            json_deserializer=orjson.loads,
            echo=True,
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine, expire_on_commit=False
        )

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory


database = Database()
