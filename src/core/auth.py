from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from .jwt import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/user/auth')

async def get_current_user(token: str = Depends(oauth2_scheme)):
    if token:
        return verify_token(token)
    raise HTTPException(401, headers={'WWW-Authenticate': 'Bearer'})

