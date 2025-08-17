from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.UserSettings)
async def read_settings(
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get the current user's settings.
    """
    settings = await crud.settings_get(db, user_id=current_user.id)
    if not settings:
        # If no settings exist, create them with default values
        settings = await crud.settings_create_or_update(
            db, obj_in=schemas.UserSettingsCreate(), user_id=current_user.id
        )
    return settings


@router.put("/", response_model=schemas.UserSettings)
async def update_settings(
    *,
    db: AsyncSession = Depends(deps.get_db),
    settings_in: schemas.UserSettingsUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update the current user's settings.
    """
    settings = await crud.settings_create_or_update(
        db, obj_in=settings_in, user_id=current_user.id
    )
    return settings
