from .base import BaseRepository
from src.models.answer import Answer

class AnswerRepository(BaseRepository[Answer]):
    table = Answer
