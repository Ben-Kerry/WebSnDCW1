from sqlalchemy.orm import Session

from app.models.match import Match


class MatchRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Match]:
        return self.db.query(Match).order_by(Match.match_date.asc()).all()

    def get(self, match_id: int) -> Match | None:
        return self.db.query(Match).filter(Match.id == match_id).first()

    def create(self, payload: dict) -> Match:
        match = Match(**payload)
        self.db.add(match)
        self.db.commit()
        self.db.refresh(match)
        return match

    def update(self, match: Match, payload: dict) -> Match:
        for key, value in payload.items():
            setattr(match, key, value)
        self.db.commit()
        self.db.refresh(match)
        return match

    def delete(self, match: Match) -> None:
        self.db.delete(match)
        self.db.commit()