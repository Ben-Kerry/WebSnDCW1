from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.team import TeamRepository
from app.repositories.team_form import TeamFormRepository


class TeamFormService:
    def __init__(self, db: Session):
        self.repo = TeamFormRepository(db)
        self.team_repo = TeamRepository(db)

    def list_forms(self):
        return self.repo.list()

    def get_form(self, form_id: int):
        form = self.repo.get(form_id)
        if not form:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team form snapshot not found")
        return form

    def create_form(self, payload: dict):
        if not self.team_repo.get(payload["team_id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid team_id")
        return self.repo.create(payload)

    def update_form(self, form_id: int, payload: dict):
        form = self.get_form(form_id)
        if "team_id" in payload and not self.team_repo.get(payload["team_id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid team_id")
        return self.repo.update(form, payload)

    def delete_form(self, form_id: int):
        form = self.get_form(form_id)
        self.repo.delete(form)