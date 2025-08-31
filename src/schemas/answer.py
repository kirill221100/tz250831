from typing import Annotated
from datetime import datetime
from pydantic import BaseModel, StringConstraints, UUID4


class AnswerBase(BaseModel):
    text: Annotated[str, StringConstraints(min_length=1)]

class AnswerResponse(AnswerBase):
    id: UUID4
    question_id: UUID4
    user_id: UUID4
    created_at: datetime