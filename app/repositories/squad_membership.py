from sqlalchemy.orm import Session

from app.models.squad_membership import SquadMembership


class SquadMembershipRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[SquadMembership]:
        return self.db.query(SquadMembership).order_by(SquadMembership.id.asc()).all()

    def get(self, membership_id: int) -> SquadMembership | None:
        return self.db.query(SquadMembership).filter(SquadMembership.id == membership_id).first()

    def create(self, payload: dict) -> SquadMembership:
        membership = SquadMembership(**payload)
        self.db.add(membership)
        self.db.commit()
        self.db.refresh(membership)
        return membership

    def update(self, membership: SquadMembership, payload: dict) -> SquadMembership:
        for key, value in payload.items():
            setattr(membership, key, value)
        self.db.commit()
        self.db.refresh(membership)
        return membership

    def delete(self, membership: SquadMembership) -> None:
        self.db.delete(membership)
        self.db.commit()