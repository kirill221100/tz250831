import pytest
from fastapi.security import OAuth2PasswordRequestForm
from httpx import AsyncClient
from pydantic import BaseModel
from src.schemas import RegistrationPayload
from src.utils.custom_types import AsyncFunc
from tests.fixtures import test_cases
from tests.unit.conftest import RegisterTestSchema


class TestUserRouter:
    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize(
        ('registration_data', 'expected_result', 'status_code', 'status_string'),
        test_cases.PARAMS_USER_ROUTE_REGISTRATION
    )
    @pytest.mark.anyio
    async def test_registration(self, registration_data: RegistrationPayload, expected_result, status_code: int,
                                status_string: str, ac: AsyncClient, get_user: AsyncFunc):
        res = await ac.post('/api/v1/user/registration', json=registration_data.model_dump())
        assert res.status_code == status_code
        if status_string:
            res = res.json()
            assert status_string in res['detail']
        else:
            db_res = await get_user(username=registration_data.username)
            res = RegisterTestSchema(**db_res.__dict__)
            assert res == expected_result



    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize(
        ('auth_data', 'response_model', 'status_code', 'status_string'),
        test_cases.PARAMS_USER_ROUTE_AUTH
    )
    @pytest.mark.anyio
    async def test_auth(self, auth_data: OAuth2PasswordRequestForm, response_model: BaseModel, status_code: int,
                        status_string: str, ac: AsyncClient, get_user: AsyncFunc):
        res = await ac.post('/api/v1/user/auth', data=auth_data.__dict__,
                            headers={"content-type": "application/x-www-form-urlencoded"})
        assert res.status_code == status_code
        res = res.json()
        if status_string:
            assert status_string in res['detail']
        else:
            assert response_model.model_validate(res)
