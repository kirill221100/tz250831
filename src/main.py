from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from src.config import cfg
from src.database import init_db
from uvicorn import run
from pathlib import Path
from src.api.routes import v1_router
from src.models import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan, debug=cfg.DEBUG, title='tz')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(v1_router)

if __name__ == '__main__':
    run(f"{Path(__file__).stem}:app", reload=cfg.RELOAD, port=8001)
