from http.client import HTTPException
from fastapi import APIRouter, Depends
from pydantic import UUID4
from starlette.status import HTTP_201_CREATED, HTTP_200_OK
from src.core.auth import get_current_user
from src.schemas import AnswerBase, AnswerResponse
from src.services.answer import AnswerService
from src.services.question import QuestionService

answer_router = APIRouter(tags=['answer'])

@answer_router.post('/questions/{question_id}/answers/', response_model=AnswerResponse, status_code=HTTP_201_CREATED)
async def create_answer(
        question_id: UUID4,
        answer_data: AnswerBase,
        user: dict = Depends(get_current_user),
        question_service: "QuestionService" = Depends(QuestionService),
        answer_service: "AnswerService" = Depends(AnswerService)
):
    if await question_service.get_question(question_id):
        return await answer_service.create_new_answer(answer_data, question_id, user["user_id"])
    raise HTTPException(404, 'No such question')

@answer_router.get('/answers/{answer_id}/', response_model=AnswerResponse, status_code=HTTP_200_OK)
async def get_answer_by_id(answer_id: UUID4, answer_service: "AnswerService" = Depends(AnswerService)):
    return await answer_service.get_answer(answer_id)

@answer_router.delete('/answers/{answer_id}/', status_code=HTTP_200_OK)
async def delete_answer_by_id(
        answer_id: UUID4,
        user: dict = Depends(get_current_user),
        answer_service: "AnswerService" = Depends(AnswerService)
):
    await answer_service.delete_answer(answer_id, user['user_id'])
    return HTTP_200_OK
