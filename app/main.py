from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.app_name}