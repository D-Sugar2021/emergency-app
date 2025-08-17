from fastapi import APIRouter

from app.api.endpoints import login, media, settings, users, vault

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(media.router, prefix="/media", tags=["media"])
api_router.include_router(vault.router, prefix="/vault", tags=["vault"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
