from .v1.question import question_router
from .v1.user import user_router
from .v1.answer import answer_router
from fastapi import APIRouter

v1_router = APIRouter(prefix='/api/v1')
v1_router.include_router(question_router)
v1_router.include_router(user_router)
v1_router.include_router(answer_router)