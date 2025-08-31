from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4
from src import database as db
from src.repositories.answer import AnswerRepository
from src.schemas import AnswerBase


class AnswerService:
    def __init__(self, session: AsyncSession = Depends(db.get_async_session)):
        self.session = session
        self.answer_repo = AnswerRepository(session=session)

    @db.transaction
    async def create_new_answer(self, answer_data: AnswerBase, question_id: UUID4, user_id: UUID4, _commit=True):
        return await self.answer_repo.add_one(**answer_data.model_dump(), question_id=question_id, user_id=user_id)

    async def get_answer(self, answer_id: UUID4):
        if not (answer := await self.answer_repo.get_filter_by_with_options_or_none(id=answer_id)):
            raise HTTPException(404)
        return answer

    @db.transaction
    async def delete_answer(self, answer_id: UUID4, user_id: UUID4, _commit=True):
        if not (answer := await self.answer_repo.get_by_query_one_or_none(id=answer_id)):
            raise HTTPException(404)
        if str(answer.user_id) == user_id:
            await self.session.delete(answer)
        else:
            raise HTTPException(403, 'You cannot delete this answer')


