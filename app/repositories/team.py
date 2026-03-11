from sqlalchemy.orm import Session

from app.models.team import Team


class TeamRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Team]:
        return self.db.query(Team).order_by(Team.name.asc()).all()

    def get(self, team_id: int) -> Team | None:
        return self.db.query(Team).filter(Team.id == team_id).first()

    def get_by_name(self, name: str) -> Team | None:
        return self.db.query(Team).filter(Team.name == name).first()

    def create(self, payload: dict) -> Team:
        team = Team(**payload)
        self.db.add(team)
        self.db.commit()
        self.db.refresh(team)
        return team

    def update(self, team: Team, payload: dict) -> Team:
        for key, value in payload.items():
            setattr(team, key, value)
        self.db.commit()
        self.db.refresh(team)
        return team

    def delete(self, team: Team) -> None:
        self.db.delete(team)
        self.db.commit()