from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PlayerAvailabilityBase(BaseModel):
    player_id: int
    team_id: int
    status: str = Field(min_length=2, max_length=30)
    reason: str | None = Field(default=None, max_length=255)
    as_of_date: datetime


class PlayerAvailabilityCreate(PlayerAvailabilityBase):
    pass


class PlayerAvailabilityUpdate(BaseModel):
    player_id: int | None = None
    team_id: int | None = None
    status: str | None = Field(default=None, min_length=2, max_length=30)
    reason: str | None = Field(default=None, max_length=255)
    as_of_date: datetime | None = None


class PlayerAvailabilityRead(PlayerAvailabilityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)