from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4
from sqlalchemy.orm import selectinload
from src import database as db
from src.repositories.question import QuestionRepository
from src.schemas import QuestionBase



class QuestionService:
    def __init__(self, session: AsyncSession = Depends(db.get_async_session)):
        self.session = session
        self.question_repo = QuestionRepository(session=session)

    async def get_all_questions(self):
        return await self.question_repo.get_all()

    @db.transaction
    async def create_new_question(self, question_data: QuestionBase, user_id: UUID4, _commit=True):
        return await self.question_repo.add_one(**question_data.model_dump(), user_id=user_id)

    async def get_question(self, question_id: UUID4):
        question = await self.question_repo.get_filter_by_with_options_or_none(
            selectinload(self.question_repo.table.answers),
            id=question_id
        )
        if not question:
            raise HTTPException(404)
        return question

    @db.transaction
    async def delete_question(self, question_id: UUID4, user_id: UUID4, _commit=True):
        question = await self.question_repo.get_by_query_one_or_none(id=question_id)
        if not question:
             raise HTTPException(404)
        if str(question.user_id) == user_id:
            await self.session.delete(question)
        else:
            raise HTTPException(403, 'You cannot delete this question')


