from .base import BaseRepository
from src.models.user import User


class UserRepository(BaseRepository[User]):
    table = User
