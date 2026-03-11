from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.match import MatchCreate, MatchRead, MatchUpdate
from app.services.match import MatchService
from app.utils.responses import success_response

router = APIRouter(prefix="/matches", tags=["Matches"])


@router.get("", response_model=dict)
def list_matches(db: Session = Depends(get_db)):
    data = [MatchRead.model_validate(match).model_dump() for match in MatchService(db).list_matches()]
    return success_response(data, "Matches retrieved")


@router.get("/{match_id}", response_model=dict)
def get_match(match_id: int, db: Session = Depends(get_db)):
    match = MatchService(db).get_match(match_id)
    return success_response(MatchRead.model_validate(match).model_dump(), "Match retrieved")


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_match(payload: MatchCreate, db: Session = Depends(get_db)):
    match = MatchService(db).create_match(payload.model_dump())
    return success_response(MatchRead.model_validate(match).model_dump(), "Match created")


@router.put("/{match_id}", response_model=dict)
def update_match(match_id: int, payload: MatchUpdate, db: Session = Depends(get_db)):
    match = MatchService(db).update_match(match_id, payload.model_dump(exclude_unset=True))
    return success_response(MatchRead.model_validate(match).model_dump(), "Match updated")


@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_match(match_id: int, db: Session = Depends(get_db)):
    MatchService(db).delete_match(match_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)