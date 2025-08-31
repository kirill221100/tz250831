from collections.abc import Callable
from functools import wraps
from src.config import cfg
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator

async_engine = create_async_engine(
    f"postgresql+asyncpg://{cfg.POSTGRES_USER}:{cfg.POSTGRES_PASSWORD}@{cfg.POSTGRES_HOST}:{cfg.POSTGRES_PORT}/{cfg.POSTGRES_DB}",
    echo=True
)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
Base = declarative_base()

def transaction(func: Callable):

    @wraps(func)
    async def wrapper(*args, **kwargs):
        _commit = kwargs.pop("_commit", True)
        result = await func(*args, **kwargs)

        self = args[0]
        if _commit:
            await self.session.commit()
        else:
            await self.session.flush()
        return result

    return wrapper

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as s:
        yield s
