from collections.abc import Sequence
from copy import deepcopy
from typing import List, Optional
from pydantic import BaseModel, UUID4
from src.schemas import AnswerBase
from tests import fixtures
from src.models import User, Question, Answer
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from tests.utils import bulk_save_models


@pytest.fixture
def users() -> tuple[dict]:
    return deepcopy(fixtures.postgres.USERS)

@pytest.fixture
def questions() -> tuple[dict]:
    return deepcopy(fixtures.postgres.QUESTIONS)

@pytest.fixture
def answers() -> tuple[dict]:
    return deepcopy(fixtures.postgres.ANSWERS)

@pytest.fixture
def first_user() -> dict:
    return deepcopy(fixtures.postgres.USERS[0])

@pytest.fixture
async def setup_users(fixture_session: AsyncSession, users: tuple[dict])-> None:
    await bulk_save_models(fixture_session, User, users)


@pytest.fixture
async def setup_questions(fixture_session: AsyncSession, questions: tuple[dict])-> None:
    await bulk_save_models(fixture_session, Question, questions)

@pytest.fixture
async def setup_answers(fixture_session: AsyncSession, answers: tuple[dict])-> None:
    await bulk_save_models(fixture_session, Answer, answers)

@pytest.fixture
def get_users(fixture_session: AsyncSession):
    async def _get_users() -> Sequence[User]:
        res = await fixture_session.execute(select(User))
        return res.scalars().all()
    return _get_users

@pytest.fixture
def get_user(fixture_session: AsyncSession):
    async def _get_user(*args, **kwargs) -> Sequence[User]:
        res = await fixture_session.execute(select(User).filter_by(**kwargs).options(*args))
        return res.scalar_one_or_none()
    return _get_user

@pytest.fixture
def get_question(fixture_session: AsyncSession):
    async def _get_question(*args, **kwargs) -> Sequence[User]:
        res = await fixture_session.execute(select(Question).filter_by(**kwargs).options(*args))
        return res.scalar_one_or_none()
    return _get_question


@pytest.fixture
def get_answer(fixture_session: AsyncSession):
    async def _get_answer(*args, **kwargs) -> Sequence[User]:
        res = await fixture_session.execute(select(Answer).filter_by(**kwargs).options(*args))
        return res.scalar_one_or_none()
    return _get_answer

class UserResponse(BaseModel):
    id: UUID4
    username: str
    hashed_password: str


class QuestionResponseTest(BaseModel):
    id: UUID4
    user_id: UUID4
    text: str

class AnswerResponseTest(AnswerBase):
    id: UUID4
    user_id: UUID4
    question_id: UUID4


class QuestionWithAnswersResponseTest(QuestionResponseTest):
    answers: Optional[List[AnswerResponseTest]]

class UserResponseWithQuestions(UserResponse):
    questions: List[QuestionResponseTest]


class RegisterTestSchema(BaseModel):
    username: str
