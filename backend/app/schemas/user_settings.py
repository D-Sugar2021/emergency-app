from typing import Optional

from pydantic import BaseModel, Field


class UserSettingsBase(BaseModel):
    chime_volume: Optional[float] = Field(1.0, ge=0.0, le=1.0)


class UserSettings(UserSettingsBase):
    pass


class UserSettingsCreate(UserSettingsBase):
    pass


class UserSettingsUpdate(UserSettingsBase):
    pass
