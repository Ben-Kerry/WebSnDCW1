from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class MatchBase(BaseModel):
    home_team_id: int
    away_team_id: int
    competition: str = Field(default="UEFA Europa League", min_length=2, max_length=100)
    match_date: datetime
    venue: str = Field(min_length=2, max_length=120)
    home_score: int | None = Field(default=None, ge=0)
    away_score: int | None = Field(default=None, ge=0)
    status: str = Field(default="scheduled", min_length=2, max_length=30)

    @model_validator(mode="after")
    def validate_teams(self):
        if self.home_team_id == self.away_team_id:
            raise ValueError("home_team_id and away_team_id must be different")
        return self


class MatchCreate(MatchBase):
    pass


class MatchUpdate(BaseModel):
    home_team_id: int | None = None
    away_team_id: int | None = None
    competition: str | None = Field(default=None, min_length=2, max_length=100)
    match_date: datetime | None = None
    venue: str | None = Field(default=None, min_length=2, max_length=120)
    home_score: int | None = Field(default=None, ge=0)
    away_score: int | None = Field(default=None, ge=0)
    status: str | None = Field(default=None, min_length=2, max_length=30)


class MatchRead(MatchBase):
    id: int

    model_config = ConfigDict(from_attributes=True)