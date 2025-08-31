from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from starlette.status import HTTP_201_CREATED, HTTP_200_OK
from src.core.auth import get_current_user
from src.schemas import QuestionResponse, QuestionBase, QuestionWithAnswersResponse
from src.services.question import QuestionService

question_router = APIRouter(prefix='/questions', tags=['question'])

@question_router.get('/', response_model=List[QuestionResponse], status_code=HTTP_200_OK)
async def get_all_questions(question_service: "QuestionService" = Depends(QuestionService)):
    return await question_service.get_all_questions()

@question_router.post('/', response_model=QuestionResponse, status_code=HTTP_201_CREATED)
async def create_question(
        question_data: QuestionBase,
        user: dict = Depends(get_current_user),
        question_service: "QuestionService" = Depends(QuestionService),
):
    return await question_service.create_new_question(question_data, user["user_id"])

@question_router.get('/{question_id}', response_model=QuestionWithAnswersResponse, status_code=HTTP_200_OK)
async def get_question_by_id(question_id: UUID4, question_service: "QuestionService" = Depends(QuestionService)):
    if not (question := await question_service.get_question(question_id)):
        raise HTTPException(404, 'No such question')
    return question


@question_router.delete('/{question_id}', status_code=HTTP_200_OK)
async def delete_question_by_id(
        question_id: UUID4,
        user: dict = Depends(get_current_user),
        question_service: "QuestionService" = Depends(QuestionService)
):
    await question_service.delete_question(question_id, user["user_id"])
    return HTTP_200_OK
