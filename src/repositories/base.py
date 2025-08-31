from typing import TypeVar, Generic, Any
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import Base

Table = TypeVar('Table', bound=Base)

class BaseRepository(Generic[Table]):
    table: type[Table]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_one(self, **kwargs: Any) -> None:
        query = insert(self.table).values(**kwargs).returning(self.table)
        return (await self.session.execute(query)).scalar_one_or_none()

    async def get_by_query_one_or_none(self, **kwargs: Any) -> Table | None:
        query = select(self.table).filter_by(**kwargs)
        res = await self.session.execute(query)
        return res.unique().scalar_one_or_none()

    async def get_all(self) -> Table | None:
        query = select(self.table)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_filter_by_with_options_or_none(self, *args, **kwargs) -> Table | None:
        query = select(self.table).filter_by(**kwargs).options(*args)
        res = await self.session.execute(query)
        return res.scalar_one_or_none()
