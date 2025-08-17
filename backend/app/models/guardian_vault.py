from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GuardianVault(Base):
    __tablename__ = "guardian_vaults"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    encrypted_data = Column(Text, nullable=False)
    user = relationship("User", back_populates="vault")
