from fastapi import FastAPI

from app.api.api import api_router
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base  # noqa: F401

app = FastAPI(
    title="Guardian AI Pro",
)

from app.tasks.example import example_task

@app.get("/health")
def read_health():
    return {"status": "ok"}

@app.post("/test-celery/", status_code=201)
def test_celery(word: str):
    """
    Test Celery task.
    """
    example_task.delay(word)
    return {"msg": "Task was sent to the background"}

@app.on_event("startup")
async def on_startup():
    # Create db tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(api_router, prefix=settings.API_V1_STR)
