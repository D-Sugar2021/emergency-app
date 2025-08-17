import datetime
from typing import List, Optional

from pydantic import BaseModel


# Shared properties
class MediaBase(BaseModel):
    filename: str | None = None


# Properties to receive on creation
class MediaCreate(BaseModel):
    filename: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    bookmarks: Optional[List[int]] = None
    tags: Optional[List[str]] = None
    capture_method: Optional[str] = None


# Properties to return to client
class Media(MediaBase):
    id: int
    owner_id: int
    created_at: datetime.datetime
    content_type: str
    size: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    bookmarks: Optional[List[int]] = None
    tags: Optional[List[str]] = None
    transcription: Optional[str] = None
    summary: Optional[str] = None
    ai_processing_status: Optional[str] = None
    capture_method: Optional[str] = None

    class Config:
        from_attributes = True
