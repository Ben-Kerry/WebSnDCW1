from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class MatchBase(BaseModel):
    home_team_id: int
    away_team_id: int
    round_name: str = Field(min_length=2, max_length=50)
    leg_number: int | None = Field(default=None, ge=1, le=2)
    bracket_slot: str | None = Field(default=None, max_length=50)
    match_date: datetime
    venue: str = Field(min_length=2, max_length=120)
    is_neutral_venue: bool = False
    home_score: int | None = Field(default=None, ge=0)
    away_score: int | None = Field(default=None, ge=0)
    status: str = Field(default="scheduled", min_length=2, max_length=30)
    winner_team_id: int | None = None

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
    round_name: str | None = Field(default=None, min_length=2, max_length=50)
    leg_number: int | None = Field(default=None, ge=1, le=2)
    bracket_slot: str | None = Field(default=None, max_length=50)
    match_date: datetime | None = None
    venue: str | None = Field(default=None, min_length=2, max_length=120)
    is_neutral_venue: bool | None = None
    home_score: int | None = Field(default=None, ge=0)
    away_score: int | None = Field(default=None, ge=0)
    status: str | None = Field(default=None, min_length=2, max_length=30)
    winner_team_id: int | None = None


class MatchRead(MatchBase):
    id: int

    model_config = ConfigDict(from_attributes=True)