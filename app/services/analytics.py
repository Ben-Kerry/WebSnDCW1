from sqlalchemy.orm import Session

from app.models.match import Match
from app.models.player import Player
from app.models.probability import Probability
from app.models.team import Team


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def leaderboard(self):
        teams = self.db.query(Team).all()
        completed_matches = self.db.query(Match).filter(Match.status == "completed").all()

        table = {
            team.id: {
                "team_id": team.id,
                "team_name": team.name,
                "wins": 0,
                "draws": 0,
                "losses": 0,
                "goals_for": 0,
                "goals_against": 0,
                "points": 0,
            }
            for team in teams
        }

        for match in completed_matches:
            if match.home_score is None or match.away_score is None:
                continue

            home = table[match.home_team_id]
            away = table[match.away_team_id]

            home["goals_for"] += match.home_score
            home["goals_against"] += match.away_score
            away["goals_for"] += match.away_score
            away["goals_against"] += match.home_score

            if match.home_score > match.away_score:
                home["wins"] += 1
                home["points"] += 3
                away["losses"] += 1
            elif match.home_score < match.away_score:
                away["wins"] += 1
                away["points"] += 3
                home["losses"] += 1
            else:
                home["draws"] += 1
                away["draws"] += 1
                home["points"] += 1
                away["points"] += 1

        return sorted(
            table.values(),
            key=lambda row: (row["points"], row["goals_for"] - row["goals_against"], row["goals_for"]),
            reverse=True,
        )

    def player_summaries(self):
        players = self.db.query(Player, Team.name.label("team_name")).join(Team, Player.team_id == Team.id).all()
        return [
            {
                "player_id": player.id,
                "player_name": player.name,
                "team_name": team_name,
                "goals": player.goals,
                "assists": player.assists,
                "rating": player.rating,
            }
            for player, team_name in players
        ]

    def probability_summary(self):
        rows = self.db.query(Probability, Team.name.label("team_name")).join(Team, Probability.team_id == Team.id).all()
        return [
            {
                "team_id": probability.team_id,
                "team_name": team_name,
                "win_probability": probability.win_probability,
                "source_confidence": probability.source_confidence,
        ]