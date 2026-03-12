from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.team_form import TeamFormCreate, TeamFormRead, TeamFormUpdate
from app.services.team_form import TeamFormService
from app.utils.responses import success_response

router = APIRouter(prefix="/team-form", tags=["Team Form"])


@router.get("", response_model=dict)
def list_forms(db: Session = Depends(get_db)):
    data = [TeamFormRead.model_validate(item).model_dump() for item in TeamFormService(db).list_forms()]
    return success_response(data, "Team form snapshots retrieved")


@router.get("/{form_id}", response_model=dict)
def get_form(form_id: int, db: Session = Depends(get_db)):
    form = TeamFormService(db).get_form(form_id)
    return success_response(TeamFormRead.model_validate(form).model_dump(), "Team form snapshot retrieved")


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_form(payload: TeamFormCreate, db: Session = Depends(get_db)):
    form = TeamFormService(db).create_form(payload.model_dump())
    return success_response(TeamFormRead.model_validate(form).model_dump(), "Team form snapshot created")


@router.put("/{form_id}", response_model=dict)
def update_form(form_id: int, payload: TeamFormUpdate, db: Session = Depends(get_db)):
    form = TeamFormService(db).update_form(form_id, payload.model_dump(exclude_unset=True))
    return success_response(TeamFormRead.model_validate(form).model_dump(), "Team form snapshot updated")


@router.delete("/{form_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_form(form_id: int, db: Session = Depends(get_db)):
    TeamFormService(db).delete_form(form_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)