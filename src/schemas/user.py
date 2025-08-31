from pydantic import BaseModel, StringConstraints
from typing import Annotated


class RegistrationPayload(BaseModel):
    username: Annotated[str, StringConstraints(min_length=2, max_length=30)]
    password: Annotated[str, StringConstraints(min_length=6, max_length=30)]

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
