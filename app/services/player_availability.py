from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.player import PlayerRepository
from app.repositories.player_availability import PlayerAvailabilityRepository
from app.repositories.team import TeamRepository


class PlayerAvailabilityService:
    def __init__(self, db: Session):
        self.repo = PlayerAvailabilityRepository(db)
        self.player_repo = PlayerRepository(db)
        self.team_repo = TeamRepository(db)

    def list_availability(self):
        return self.repo.list()

    def get_availability(self, availability_id: int):
        availability = self.repo.get(availability_id)
        if not availability:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Availability record not found")
        return availability

    def create_availability(self, payload: dict):
        if not self.player_repo.get(payload["player_id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid player_id")
        if not self.team_repo.get(payload["team_id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid team_id")
        return self.repo.create(payload)

    def update_availability(self, availability_id: int, payload: dict):
        availability = self.get_availability(availability_id)
        if "player_id" in payload and not self.player_repo.get(payload["player_id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid player_id")
        if "team_id" in payload and not self.team_repo.get(payload["team_id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid team_id")
        return self.repo.update(availability, payload)

    def delete_availability(self, availability_id: int):
        availability = self.get_availability(availability_id)
        self.repo.delete(availability)