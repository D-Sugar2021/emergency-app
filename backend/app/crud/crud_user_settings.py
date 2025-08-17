from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user_settings import UserSettings
from app.schemas.user_settings import UserSettingsCreate, UserSettingsUpdate


async def get(db: AsyncSession, *, user_id: int) -> UserSettings | None:
    result = await db.execute(
        select(UserSettings).filter(UserSettings.user_id == user_id)
    )
    return result.scalars().first()


async def create_or_update(
    db: AsyncSession, *, obj_in: UserSettingsCreate, user_id: int
) -> UserSettings:
    result = await db.execute(
        select(UserSettings).filter(UserSettings.user_id == user_id)
    )
    db_obj = result.scalars().first()

    if db_obj:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
    else:
        db_obj = UserSettings(**obj_in.model_dump(), user_id=user_id)

    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
