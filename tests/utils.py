from collections.abc import Iterable, Sequence
from copy import copy
from typing import Any
from pydantic import BaseModel
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


async def bulk_save_models(
        session: AsyncSession,
        model: type[DeclarativeBase],
        data: Iterable[dict[str, Any]]
) -> None:
    for val in data:
        if 'relationships' in val:
            val = copy(val)
            del val['relationships']
        await session.execute(insert(model).values(**val))

    await session.flush()

def compare_dicts_and_db_models(
        result: Sequence[DeclarativeBase] | None,
        expected_result: Sequence[dict] | None,
        schema: type[BaseModel]
) -> bool:
    if result is None or expected_result is None:
        return result == expected_result

    result_to_schema = [schema(**item.__dict__) for item in result]
    expected_result_to_schema = [schema(**item) for item in expected_result]

    equality_len = len(result_to_schema) == len(expected_result_to_schema)
    equality_obj = all(obj in expected_result_to_schema for obj in result_to_schema)
    return all((equality_len, equality_obj))

