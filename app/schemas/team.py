from pydantic import BaseModel, ConfigDict, Field


class TeamBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    country: str = Field(min_length=2, max_length=100)
    coach: str | None = Field(default=None, max_length=100)
    founded_year: int | None = Field(default=None, ge=1800, le=2100)
    uefa_coefficient: float = Field(default=0.0, ge=0)


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    country: str | None = Field(default=None, min_length=2, max_length=100)
    coach: str | None = Field(default=None, max_length=100)
    founded_year: int | None = Field(default=None, ge=1800, le=2100)
    uefa_coefficient: float | None = Field(default=None, ge=0)


class TeamRead(TeamBase):
    id: int

    model_config = ConfigDict(from_attributes=True)