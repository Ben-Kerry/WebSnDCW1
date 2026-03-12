from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.player import PlayerRepository
from app.repositories.squad_membership import SquadMembershipRepository
from app.repositories.team import TeamRepository


class SquadMembershipService:
    def __init__(self, db: Session):
        self.repo = SquadMembershipRepository(db)
        self.player_repo = PlayerRepository(db)
        self.team_repo = TeamRepository(db)

    def list_memberships(self):
        return self.repo.list()

    def get_membership(self, membership_id: int):
        membership = self.repo.get(membership_id)
        if not membership:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Squad membership not found")
        return membership

    def create_membership(self, payload: dict):
        if not self.player_repo.get(payload["player_id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid player_id")
        if not self.team_repo.get(payload["team_id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid team_id")
        return self.repo.create(payload)

    def update_membership(self, membership_id: int, payload: dict):
        membership = self.get_membership(membership_id)
        if "player_id" in payload and not self.player_repo.get(payload["player_id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid player_id")
        if "team_id" in payload and not self.team_repo.get(payload["team_id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid team_id")
        return self.repo.update(membership, payload)

    def delete_membership(self, membership_id: int):
        membership = self.get_membership(membership_id)
        self.repo.delete(membership)