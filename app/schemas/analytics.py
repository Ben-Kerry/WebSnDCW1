from pydantic import BaseModel


class LeaderboardEntry(BaseModel):
    team_id: int
    team_name: str
    wins: int
    draws: int
    losses: int
    goals_for: int
    goals_against: int
    points: int


class PlayerSummary(BaseModel):
    player_id: int
    player_name: str
    team_name: str
    goals: int
    assists: int
    rating: float


class TeamProbabilitySummary(BaseModel):
    team_id: int
    team_name: str
    win_probability: float
    source_confidence: float