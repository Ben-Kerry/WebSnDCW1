from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.team import TeamRepository


class TeamService:
    def __init__(self, db: Session):
        self.repo = TeamRepository(db)

    def list_teams(self):
        return self.repo.list()

    def get_team(self, team_id: int):
        team = self.repo.get(team_id)
        if not team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
        return team

    def create_team(self, payload: dict):
        if self.repo.get_by_name(payload["name"]):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Team already exists")
        return self.repo.create(payload)

    def update_team(self, team_id: int, payload: dict):
        team = self.get_team(team_id)
        return self.repo.update(team, payload)

    def delete_team(self, team_id: int):
        team = self.get_team(team_id)
        self.repo.delete(team)