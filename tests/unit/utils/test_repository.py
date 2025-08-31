from tests.fixtures import test_cases
from sqlalchemy.ext.asyncio import AsyncSession
from tests.unit.conftest import UserResponse, UserResponseWithQuestions
from src.utils.custom_types import AsyncFunc
from src.models import User
from src.repositories.base import BaseRepository
import pytest
from typing import Any
from tests.utils import compare_dicts_and_db_models


class TestBaseRepository:
    class _BaseRepository(BaseRepository):
        table = User

    def __get_rep(self, session: AsyncSession) -> BaseRepository:
        return self._BaseRepository(session)

    @pytest.mark.anyio
    async def test_add_one(self, fixture_session: AsyncSession, first_user: dict, get_users: AsyncFunc):
        await self.__get_rep(fixture_session).add_one(**first_user)
        assert compare_dicts_and_db_models(await get_users(), [first_user], UserResponse)

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize(
        ('values', 'expected_result', 'expectation'),
        test_cases.PARAMS_TEST_REPOSITORY_GET_BY_QUERY_ONE_OR_NONE
    )
    @pytest.mark.anyio
    async def test_get_by_query_one_or_none(self, values: dict, expected_result: UserResponse, expectation: Any,
                                            fixture_session: AsyncSession, first_user: dict):
        with expectation:
            user_in_db: User | None = await self.__get_rep(fixture_session).get_by_query_one_or_none(**values)
            result = None if not user_in_db else UserResponse(**user_in_db.__dict__)
            assert result == expected_result

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.anyio
    async def test_get_all(self, fixture_session: AsyncSession, users: tuple[dict]):
        res = await self.__get_rep(fixture_session).get_all()
        assert compare_dicts_and_db_models(res, users, UserResponse)

    @pytest.mark.usefixtures('setup_users', 'setup_questions')
    @pytest.mark.parametrize(
        ('filters', 'options', 'expected_result', 'expectation'),
        test_cases.PARAMS_TEST_REPOSITORY_GET_FILTER_BY_WITH_OPTIONS_OR_NONE
    )
    @pytest.mark.anyio
    async def test_get_filter_by_with_options_or_none(self, filters, options,
                                                      expected_result: UserResponseWithQuestions,
                                                      expectation: Any,
                                                      fixture_session: AsyncSession):
        with expectation:
            user_in_db: User | None = await self.__get_rep(fixture_session).get_filter_by_with_options_or_none(
                *filters, **options)
            result = None if not user_in_db else UserResponseWithQuestions.model_validate(user_in_db.__dict__, from_attributes=True)
            assert result == expected_result
