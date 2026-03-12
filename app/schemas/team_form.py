from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TeamFormBase(BaseModel):
    team_id: int
    as_of_date: datetime
    last_5_wins: int = Field(default=0, ge=0, le=5)
    last_5_draws: int = Field(default=0, ge=0, le=5)
    last_5_losses: int = Field(default=0, ge=0, le=5)
    last_5_goals_for: int = Field(default=0, ge=0)
    last_5_goals_against: int = Field(default=0, ge=0)
    home_form_rating: float = Field(default=0.0, ge=0)
    away_form_rating: float = Field(default=0.0, ge=0)


class TeamFormCreate(TeamFormBase):
    pass


class TeamFormUpdate(BaseModel):
    team_id: int | None = None
    as_of_date: datetime | None = None
    last_5_wins: int | None = Field(default=None, ge=0, le=5)
    last_5_draws: int | None = Field(default=None, ge=0, le=5)
    last_5_losses: int | None = Field(default=None, ge=0, le=5)
    last_5_goals_for: int | None = Field(default=None, ge=0)
    last_5_goals_against: int | None = Field(default=None, ge=0)
    home_form_rating: float | None = Field(default=None, ge=0)
    away_form_rating: float | None = Field(default=None, ge=0)


class TeamFormRead(TeamFormBase):
    id: int

    model_config = ConfigDict(from_attributes=True)