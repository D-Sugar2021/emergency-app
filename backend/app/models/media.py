import datetime

from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    content_type = Column(String)
    size = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    bookmarks = Column(JSON, nullable=True)
    tags = Column(JSON, nullable=True)

    transcription = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    ai_processing_status = Column(String, default="pending")

    owner = relationship("User")
