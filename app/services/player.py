from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.player import PlayerRepository
from app.repositories.team import TeamRepository


class PlayerService:
    def __init__(self, db: Session):
        self.repo = PlayerRepository(db)
        self.team_repo = TeamRepository(db)

    def list_players(self):
        return self.repo.list()

    def get_player(self, player_id: int):
        player = self.repo.get(player_id)
        if not player:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
        return player

    def create_player(self, payload: dict):
        if not self.team_repo.get(payload["team_id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid team_id")
        return self.repo.create(payload)

    def update_player(self, player_id: int, payload: dict):
        player = self.get_player(player_id)
        if "team_id" in payload and not self.team_repo.get(payload["team_id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid team_id")
        return self.repo.update(player, payload)

    def delete_player(self, player_id: int):
        player = self.get_player(player_id)
        self.repo.delete(player)