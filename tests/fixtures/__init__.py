from collections.abc import Callable
from functools import wraps
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import RegistrationPayload, AnswerBase, QuestionBase
from src.services import user as user_module, question as question_module, answer as answer_module
from tests.fixtures import postgres

__all__ = (
    'postgres', 'FakeUserService', 'FakeAnswerService', 'FakeQuestionService'
)

def override_transaction(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        self = args[0]
        await self.session.flush()
        return result

    return wrapper

class FakeUserService(user_module.UserService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    @override_transaction
    async def create_user(self, user: RegistrationPayload, _commit=True):
        f = super().create_user.__wrapped__
        return await f(self, user, _commit)

class FakeQuestionService(question_module.QuestionService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    @override_transaction
    async def create_new_question(self, question_data: QuestionBase, user_id: UUID4, _commit=True):
        f = super().create_new_question.__wrapped__
        return await f(self, question_data, user_id, _commit)

    @override_transaction
    async def delete_question(self, question_id: UUID4, user_id: UUID4, _commit=True):
        f = super().delete_question.__wrapped__
        return await f(self, question_id, user_id, _commit)


class FakeAnswerService(answer_module.AnswerService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    @override_transaction
    async def create_new_answer(self, answer_data: AnswerBase, question_id: UUID4, user_id: UUID4, _commit=True):
        f = super().create_new_answer.__wrapped__
        return await f(self, answer_data, question_id, user_id, _commit)

    @override_transaction
    async def delete_answer(self, answer_id: UUID4, user_id: UUID4, _commit=True):
        f = super().delete_answer.__wrapped__
        return await f(self, answer_id, user_id, _commit)
