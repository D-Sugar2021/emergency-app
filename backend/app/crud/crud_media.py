from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.media import Media
from app.schemas.media import MediaCreate


async def get(db: AsyncSession, id: int) -> Media | None:
    result = await db.execute(select(Media).filter(Media.id == id))
    return result.scalars().first()


async def get_multi_by_owner(
    db: AsyncSession, *, owner_id: int, skip: int = 0, limit: int = 100
) -> List[Media]:
    result = await db.execute(
        select(Media)
        .filter(Media.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def create_with_owner(
    db: AsyncSession, *, obj_in: MediaCreate, owner_id: int, size: int, content_type: str
) -> Media:
    db_obj = Media(
        **obj_in.model_dump(),
        owner_id=owner_id,
        size=size,
        content_type=content_type,
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def remove(db: AsyncSession, *, id: int) -> Media | None:
    result = await db.execute(select(Media).filter(Media.id == id))
    obj = result.scalars().first()
    if obj:
        await db.delete(obj)
        await db.commit()
    return obj
