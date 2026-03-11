from sqlalchemy.orm import Session

from app.models.player import Player


class PlayerRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Player]:
        return self.db.query(Player).order_by(Player.name.asc()).all()

    def get(self, player_id: int) -> Player | None:
        return self.db.query(Player).filter(Player.id == player_id).first()

    def create(self, payload: dict) -> Player:
        player = Player(**payload)
        self.db.add(player)
        self.db.commit()
        self.db.refresh(player)
        return player

    def update(self, player: Player, payload: dict) -> Player:
        for key, value in payload.items():
            setattr(player, key, value)
        self.db.commit()
        self.db.refresh(player)
        return player

    def delete(self, player: Player) -> None:
        self.db.delete(player)
        self.db.commit()