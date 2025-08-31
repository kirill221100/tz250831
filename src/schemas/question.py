from typing import Annotated, List, Optional
from datetime import datetime
from pydantic import BaseModel, StringConstraints, UUID4
from src.schemas import AnswerResponse


class QuestionBase(BaseModel):
    text: Annotated[str, StringConstraints(min_length=5)]

class QuestionResponse(QuestionBase):
    id: UUID4
    user_id: UUID4
    created_at: datetime

class QuestionWithAnswersResponse(QuestionResponse):
    answers: Optional[List[AnswerResponse]]