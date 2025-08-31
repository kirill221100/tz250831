from .base import BaseRepository
from src.models.question import Question

class QuestionRepository(BaseRepository[Question]):
    table = Question
