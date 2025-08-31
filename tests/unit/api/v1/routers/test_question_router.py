import json
import pytest
from httpx import AsyncClient
from pydantic import UUID4
from src.schemas import QuestionBase
from src.utils.custom_types import AsyncFunc
from tests.fixtures import test_cases
from tests.unit.conftest import QuestionWithAnswersResponseTest


class TestQuestionRouter:
    @pytest.mark.usefixtures('setup_users', 'setup_questions')
    @pytest.mark.anyio
    async def test_get_all_questions(self, ac: AsyncClient, questions: tuple[dict]):
        res = await ac.get('/api/v1/questions/')
        assert res.status_code == 200
        assert len(res.json()) == len(questions)

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize(
        ('headers', 'question_data', 'expected_result', 'status_code'),
        test_cases.PARAMS_QUESTION_ROUTE_CREATE_QUESTION
    )
    @pytest.mark.anyio
    async def test_create_question(self, headers: dict, question_data: QuestionBase, expected_result, status_code: int,
                                ac: AsyncClient, get_question: AsyncFunc):
        res = await ac.post('/api/v1/questions/', headers=headers, json=json.loads(question_data.model_dump_json()))
        assert res.status_code == status_code
        assert res.json()['text'] == question_data.text
        assert await get_question(text=question_data.model_dump()['text'])

    @pytest.mark.usefixtures('setup_users', 'setup_questions', 'setup_answers')
    @pytest.mark.parametrize(
        ('question_id', 'expected_result', 'status_code'),
        test_cases.PARAMS_QUESTION_ROUTE_GET_QUESTION_BY_ID
    )
    @pytest.mark.anyio
    async def test_get_question_by_id(self, question_id: UUID4, expected_result, status_code: int,
                                   ac: AsyncClient):
        res = await ac.get(f'/api/v1/questions/{question_id}')
        assert res.status_code == status_code
        if expected_result:
           assert expected_result == QuestionWithAnswersResponseTest.model_validate(res.json())

    @pytest.mark.usefixtures('setup_users', 'setup_questions', 'setup_answers')
    @pytest.mark.parametrize(
        ('headers', 'question_id', 'check_result', 'status_code'),
        test_cases.PARAMS_QUESTION_ROUTE_DELETE_QUESTION_BY_ID
    )
    @pytest.mark.anyio
    async def test_delete_question_by_id(self, headers, question_id: UUID4, check_result, status_code: int,
                                      ac: AsyncClient, get_question: AsyncFunc):
        res = await ac.delete(f'/api/v1/questions/{question_id}', headers=headers)
        assert res.status_code == status_code
        if check_result:
            assert not await get_question(id=question_id)