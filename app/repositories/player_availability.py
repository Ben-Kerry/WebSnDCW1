from sqlalchemy.orm import Session

from app.models.player_availability import PlayerAvailability


class PlayerAvailabilityRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[PlayerAvailability]:
        return self.db.query(PlayerAvailability).order_by(PlayerAvailability.as_of_date.desc()).all()

    def get(self, availability_id: int) -> PlayerAvailability | None:
        return self.db.query(PlayerAvailability).filter(PlayerAvailability.id == availability_id).first()

    def create(self, payload: dict) -> PlayerAvailability:
        availability = PlayerAvailability(**payload)
        self.db.add(availability)
        self.db.commit()
        self.db.refresh(availability)
        return availability

    def update(self, availability: PlayerAvailability, payload: dict) -> PlayerAvailability:
        for key, value in payload.items():
            setattr(availability, key, value)
        self.db.commit()
        self.db.refresh(availability)
        return availability

    def delete(self, availability: PlayerAvailability) -> None:
        self.db.delete(availability)
        self.db.commit()