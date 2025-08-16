import os
import shutil
from typing import Any, List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Media])
async def read_media(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Retrieve media.
    """
    media = await crud.crud_media.get_multi_by_owner(
        db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return media


@router.post("/", response_model=schemas.Media)
async def create_upload_file(
    *,
    db: AsyncSession = Depends(deps.get_db),
    file: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new media by uploading a file.
    """
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if ".." in file.filename or file.filename.startswith("/"):
        raise HTTPException(status_code=400, detail="Invalid filename")

    file_path = os.path.join(upload_dir, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

    media_in = schemas.MediaCreate(filename=file.filename)
    media = await crud.crud_media.create_with_owner(
        db=db,
        obj_in=media_in,
        owner_id=current_user.id,
        size=file_size,
        content_type=file.content_type,
    )
    return media


@router.get("/{id}", response_model=schemas.Media)
async def read_media_item(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get media by ID.
    """
    media = await crud.crud_media.get(db=db, id=id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    if media.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return media


@router.delete("/{id}", response_model=schemas.Media)
async def delete_media_item(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a media item.
    """
    media = await crud.crud_media.get(db=db, id=id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    if media.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Also delete the file from the filesystem
    upload_dir = "uploads"
    file_path = os.path.join(upload_dir, media.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    media = await crud.crud_media.remove(db=db, id=id)
    return media
