import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from pydantic_settings import SettingsConfigDict
from pathlib import Path
from sqlalchemy import NullPool
import pytest
from src import database as db
from src.config import cfg, Config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


Config.model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent.resolve().joinpath('.env'))
test_async_engine = create_async_engine(
    f"postgresql+asyncpg://{cfg.POSTGRES_USER}:{cfg.POSTGRES_PASSWORD}@{cfg.POSTGRES_TEST_HOST}:{cfg.POSTGRES_PORT}/{cfg.POSTGRES_TEST_DB}",
    echo=False, poolclass=NullPool)
test_async_session = async_sessionmaker(test_async_engine, expire_on_commit=False)
from src.models import *

db.Base.metadata.bind = test_async_engine

from src.main import app

app.dependency_overrides[db.get_async_session] = lambda: fixture_session


@pytest.fixture(scope='function')
async def fixture_session():
    async with test_async_session() as s:
        yield s
        await s.rollback()
        await s.reset()


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope='session', autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


base_url = 'http://test'

from tests.fixtures import FakeUserService, FakeQuestionService, FakeAnswerService
from src.api.routes.v1 import user, question, answer


@pytest.fixture(autouse=True, scope='session')
async def lifespan():
    async with test_async_engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.drop_all)
        await conn.run_sync(db.Base.metadata.create_all)
    yield


client = TestClient(app)


@pytest.fixture(scope='function')
async def fake_user_service(fixture_session: AsyncSession):
    _fake = FakeUserService(fixture_session)
    yield _fake

@pytest.fixture(scope='function')
async def fake_question_service(fixture_session: AsyncSession):
    _fake = FakeQuestionService(fixture_session)
    yield _fake

@pytest.fixture(scope='function')
async def fake_answer_service(fixture_session: AsyncSession):
    _fake = FakeAnswerService(fixture_session)
    yield _fake

@pytest.fixture(scope='function')
async def ac(
        fake_user_service: FakeUserService,
        fake_question_service: FakeQuestionService,
        fake_answer_service: FakeAnswerService
) -> AsyncGenerator[AsyncClient, None]:
    app.router.lifespan_context = lifespan
    app.dependency_overrides[user.UserService] = lambda: fake_user_service
    app.dependency_overrides[question.QuestionService] = lambda: fake_question_service
    app.dependency_overrides[answer.AnswerService] = lambda: fake_answer_service
    async with AsyncClient(base_url=base_url, transport=ASGITransport(app=app)) as c:
        yield c

