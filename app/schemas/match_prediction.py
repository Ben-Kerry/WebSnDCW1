from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class MatchPredictionBase(BaseModel):
    match_id: int
    model_name: str = Field(min_length=1, max_length=80)
    model_version: str = Field(min_length=1, max_length=40)
    generated_at: datetime
    home_win_probability: float = Field(ge=0, le=1)
    draw_probability: float = Field(ge=0, le=1)
    away_win_probability: float = Field(ge=0, le=1)
    predicted_home_goals: float | None = Field(default=None, ge=0)
    predicted_away_goals: float | None = Field(default=None, ge=0)
    confidence_score: float | None = Field(default=None, ge=0, le=1)

    @model_validator(mode="after")
    def validate_probabilities(self):
        total = self.home_win_probability + self.draw_probability + self.away_win_probability
        if abs(total - 1.0) > 0.02:
            raise ValueError("home/draw/away probabilities must sum to 1.0")
        return self


class MatchPredictionCreate(MatchPredictionBase):
    pass


class MatchPredictionUpdate(BaseModel):
    match_id: int | None = None
    model_name: str | None = Field(default=None, min_length=1, max_length=80)
    model_version: str | None = Field(default=None, min_length=1, max_length=40)
    generated_at: datetime | None = None
    home_win_probability: float | None = Field(default=None, ge=0, le=1)
    draw_probability: float | None = Field(default=None, ge=0, le=1)
    away_win_probability: float | None = Field(default=None, ge=0, le=1)
    predicted_home_goals: float | None = Field(default=None, ge=0)
    predicted_away_goals: float | None = Field(default=None, ge=0)
    confidence_score: float | None = Field(default=None, ge=0, le=1)


class MatchPredictionRead(MatchPredictionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)