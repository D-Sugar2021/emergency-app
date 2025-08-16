import datetime
from pydantic import BaseModel

# Shared properties
class MediaBase(BaseModel):
    filename: str | None = None

# Properties to receive on creation
class MediaCreate(MediaBase):
    filename: str

# Properties to return to client
class Media(MediaBase):
    id: int
    owner_id: int
    created_at: datetime.datetime
    content_type: str
    size: int

    class Config:
        from_attributes = True
