from typing import List
from sqlalchemy import String
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.utils.custom_types import uuid_pk


class User(Base):
    __tablename__ = 'users'
    id: Mapped[uuid_pk]
    username: Mapped[str] = mapped_column(String(30), unique=True)
    hashed_password: Mapped[str]
    questions: Mapped[List["Question"]] = relationship(back_populates="user", uselist=True)
    answers: Mapped[List["Answer"]] = relationship(back_populates="user", uselist=True)