from typing import List
from src.database import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from src.utils.custom_types import uuid_pk, uuid_no_pk
from sqlalchemy import Text, DateTime, ForeignKey
from datetime import datetime, timezone

class Question(Base):
    __tablename__ = 'questions'
    id: Mapped[uuid_pk]
    text: Mapped[str] = mapped_column(Text(), nullable=False)
    user_id: Mapped[uuid_no_pk] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped["User"] = relationship(back_populates="questions")
    answers: Mapped[List["Answer"]] = relationship(back_populates="question", uselist=True, cascade='all, delete')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
