from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.jwt import create_access_token
from src import database as db
from src.repositories.user import UserRepository
from src.core.password import hash_password, verify_pass
from src.schemas import RegistrationPayload


class UserService:
    def __init__(self, session: AsyncSession = Depends(db.get_async_session)):
        self.session = session
        self.user_repo = UserRepository(session=session)

    @db.transaction
    async def create_user(self, user: RegistrationPayload, _commit=True):
        if await self.user_repo.get_by_query_one_or_none(username=user.username):
            raise HTTPException(status_code=409, detail='Username already registered')
        await self.user_repo.add_one(username=user.username, hashed_password=hash_password(user.password))

    async def auth_user(self, user: OAuth2PasswordRequestForm):
        if res := await self.user_repo.get_by_query_one_or_none(username=user.username):
            user_id = str(res.id)
            hashed_password = res.hashed_password
        else:
            raise HTTPException(status_code=404, detail='No such user')
        if verify_pass(user.password, hashed_password):
            data = {'user_id': user_id}
            return {'access_token': create_access_token(data), 'token_type': 'bearer'}
        raise HTTPException(status_code=401, detail='Incorrect password')
