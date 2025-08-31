from src.database import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from src.utils.custom_types import uuid_pk, uuid_no_pk
from sqlalchemy import Text, DateTime, ForeignKey
from datetime import datetime, timezone

class Answer(Base):
    __tablename__ = 'answers'
    id: Mapped[uuid_pk]
    text: Mapped[str] = mapped_column(Text(), nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped["User"] = relationship(back_populates="answers")
    question_id: Mapped[uuid_no_pk] = mapped_column(ForeignKey('questions.id'), nullable=False)
    question: Mapped["Question"] = relationship(back_populates="answers", )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
