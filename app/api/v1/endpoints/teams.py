from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.team import TeamCreate, TeamRead, TeamUpdate
from app.services.team import TeamService
from app.utils.responses import success_response

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.get("", response_model=dict)
def list_teams(db: Session = Depends(get_db)):
    data = [TeamRead.model_validate(team).model_dump() for team in TeamService(db).list_teams()]
    return success_response(data, "Teams retrieved")


@router.get("/{team_id}", response_model=dict)
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = TeamService(db).get_team(team_id)
    return success_response(TeamRead.model_validate(team).model_dump(), "Team retrieved")


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_team(payload: TeamCreate, db: Session = Depends(get_db)):
    team = TeamService(db).create_team(payload.model_dump())
    return success_response(TeamRead.model_validate(team).model_dump(), "Team created")


@router.put("/{team_id}", response_model=dict)
def update_team(team_id: int, payload: TeamUpdate, db: Session = Depends(get_db)):
    team = TeamService(db).update_team(team_id, payload.model_dump(exclude_unset=True))
    return success_response(TeamRead.model_validate(team).model_dump(), "Team updated")


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    TeamService(db).delete_team(team_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)