from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.match import MatchRepository
from app.repositories.team import TeamRepository


class MatchService:
    def __init__(self, db: Session):
        self.repo = MatchRepository(db)
        self.team_repo = TeamRepository(db)

    def list_matches(self):
        return self.repo.list()

    def get_match(self, match_id: int):
        match = self.repo.get(match_id)
        if not match:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
        return match

    def create_match(self, payload: dict):
        if payload["home_team_id"] == payload["away_team_id"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Teams must be different")
        if not self.team_repo.get(payload["home_team_id"]) or not self.team_repo.get(payload["away_team_id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid team reference")
        return self.repo.create(payload)

    def update_match(self, match_id: int, payload: dict):
        match = self.get_match(match_id)
        return self.repo.update(match, payload)

    def delete_match(self, match_id: int):
        match = self.get_match(match_id)
        self.repo.delete(match)