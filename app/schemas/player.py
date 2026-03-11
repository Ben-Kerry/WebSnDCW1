from pydantic import BaseModel, ConfigDict, Field


class PlayerBase(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    position: str = Field(min_length=2, max_length=50)
    nationality: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=15, le=60)
    goals: int = Field(default=0, ge=0)
    assists: int = Field(default=0, ge=0)
    rating: float = Field(default=0.0, ge=0, le=10)
    team_id: int


class PlayerCreate(PlayerBase):
    pass


class PlayerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    position: str | None = Field(default=None, min_length=2, max_length=50)
    nationality: str | None = Field(default=None, min_length=2, max_length=100)
    age: int | None = Field(default=None, ge=15, le=60)
    goals: int | None = Field(default=None, ge=0)
    assists: int | None = Field(default=None, ge=0)
    rating: float | None = Field(default=None, ge=0, le=10)
    team_id: int | None = None


class PlayerRead(PlayerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)