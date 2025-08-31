import json
import pytest
from httpx import AsyncClient
from pydantic import UUID4
from src.utils.custom_types import AsyncFunc
from tests.fixtures import test_cases
from tests.unit.conftest import AnswerResponseTest


class TestAnswerRouter:
    @pytest.mark.usefixtures('setup_users', 'setup_questions')
    @pytest.mark.parametrize(
        ('headers', 'question_id', 'check_result', 'answer_data', 'status_code'),
        test_cases.PARAMS_ANSWER_ROUTE_CREATE_ANSWER
    )
    @pytest.mark.anyio
    async def test_create_answer(self, headers: dict, question_id: UUID4, check_result, answer_data,
                                   status_code: int, ac: AsyncClient, get_answer: AsyncFunc):
        res = await ac.post(
            f'/api/v1/questions/{question_id}/answers/', headers=headers, json=json.loads(answer_data.model_dump_json())
        )
        assert res.status_code == status_code
        if check_result:
            assert res.json()['text'] == answer_data.text
            assert res.json()['question_id'] == str(question_id)
            assert await get_answer(text=answer_data.text, question_id=question_id)

    @pytest.mark.usefixtures('setup_users', 'setup_questions', 'setup_answers')
    @pytest.mark.parametrize(
        ('answer_id', 'expected_result', 'status_code'),
        test_cases.PARAMS_ANSWER_ROUTE_GET_ANSWER_BY_ID
    )
    @pytest.mark.anyio
    async def test_get_answer_by_id(self, answer_id: UUID4, expected_result, status_code: int,
                                      ac: AsyncClient):
        res = await ac.get(f'/api/v1/answers/{answer_id}/')
        assert res.status_code == status_code
        if expected_result:
            assert expected_result == AnswerResponseTest.model_validate(res.json())

    @pytest.mark.usefixtures('setup_users', 'setup_questions', 'setup_answers')
    @pytest.mark.parametrize(
        ('headers', 'answer_id', 'check_result', 'status_code'),
        test_cases.PARAMS_ANSWER_ROUTE_DELETE_ANSWER_BY_ID
    )
    @pytest.mark.anyio
    async def test_delete_answer_by_id(self, headers, answer_id: UUID4, check_result, status_code: int,
                                         ac: AsyncClient, get_answer: AsyncFunc):
        res = await ac.delete(f'/api/v1/answers/{answer_id}/', headers=headers)
        assert res.status_code == status_code
        if check_result:
            assert not await get_answer(id=answer_id)


