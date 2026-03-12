from sqlalchemy.orm import Session

from app.models.team_form import TeamForm


class TeamFormRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[TeamForm]:
        return self.db.query(TeamForm).order_by(TeamForm.as_of_date.desc()).all()

    def get(self, form_id: int) -> TeamForm | None:
        return self.db.query(TeamForm).filter(TeamForm.id == form_id).first()

    def create(self, payload: dict) -> TeamForm:
        form = TeamForm(**payload)
        self.db.add(form)
        self.db.commit()
        self.db.refresh(form)
        return form

    def update(self, form: TeamForm, payload: dict) -> TeamForm:
        for key, value in payload.items():
            setattr(form, key, value)
        self.db.commit()
        self.db.refresh(form)
        return form

    def delete(self, form: TeamForm) -> None:
        self.db.delete(form)
        self.db.commit()