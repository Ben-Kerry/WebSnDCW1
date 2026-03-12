from pydantic import BaseModel, ConfigDict, Field


class SquadMembershipBase(BaseModel):
    team_id: int
    player_id: int
    shirt_number: int | None = Field(default=None, ge=1, le=99)
    is_registered: bool = True
    is_active: bool = True


class SquadMembershipCreate(SquadMembershipBase):
    pass


class SquadMembershipUpdate(BaseModel):
    team_id: int | None = None
    player_id: int | None = None
    shirt_number: int | None = Field(default=None, ge=1, le=99)
    is_registered: bool | None = None
    is_active: bool | None = None


class SquadMembershipRead(SquadMembershipBase):
    id: int

    model_config = ConfigDict(from_attributes=True)