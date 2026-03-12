from pydantic import BaseModel, ConfigDict


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


class MatchPredictionSummary(BaseModel):
    prediction_id: int
    match_id: int
    model_name: str
    model_version: str
    home_team: str
    away_team: str
    home_win_probability: float
    draw_probability: float
    away_win_probability: float
    confidence_score: float | None

    model_config = ConfigDict(protected_namespaces=())