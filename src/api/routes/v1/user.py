from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED, HTTP_200_OK
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas import RegistrationPayload, AuthResponse
from src.services.user import UserService

user_router = APIRouter(prefix='/user', tags=['user'])

@user_router.post('/registration', status_code=HTTP_201_CREATED)
async def registration(user: RegistrationPayload, user_service: "UserService"= Depends(UserService)):
    await user_service.create_user(user)
    return HTTP_201_CREATED


@user_router.post('/auth', response_model=AuthResponse, status_code=HTTP_200_OK)
async def auth(user: OAuth2PasswordRequestForm = Depends(), user_service: "UserService" = Depends(UserService)):
    return await user_service.auth_user(user)
