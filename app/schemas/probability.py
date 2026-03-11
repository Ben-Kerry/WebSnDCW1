from pydantic import BaseModel, ConfigDict, Field


class ProbabilityBase(BaseModel):
    team_id: int
    win_probability: float = Field(ge=0, le=1)
    source_confidence: float = Field(default=0.5, ge=0, le=1)


class ProbabilityCreate(ProbabilityBase):
    pass


class ProbabilityUpdate(BaseModel):
    team_id: int | None = None
    win_probability: float | None = Field(default=None, ge=0, le=1)
    source_confidence: float | None = Field(default=None, ge=0, le=1)


class ProbabilityRead(ProbabilityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)