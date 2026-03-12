from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.player_availability import PlayerAvailabilityCreate, PlayerAvailabilityRead, PlayerAvailabilityUpdate
from app.services.player_availability import PlayerAvailabilityService
from app.utils.responses import success_response

router = APIRouter(prefix="/player-availability", tags=["Player Availability"])


@router.get("", response_model=dict)
def list_availability(db: Session = Depends(get_db)):
    data = [PlayerAvailabilityRead.model_validate(item).model_dump() for item in PlayerAvailabilityService(db).list_availability()]
    return success_response(data, "Availability records retrieved")


@router.get("/{availability_id}", response_model=dict)
def get_availability(availability_id: int, db: Session = Depends(get_db)):
    record = PlayerAvailabilityService(db).get_availability(availability_id)
    return success_response(PlayerAvailabilityRead.model_validate(record).model_dump(), "Availability record retrieved")


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_availability(payload: PlayerAvailabilityCreate, db: Session = Depends(get_db)):
    record = PlayerAvailabilityService(db).create_availability(payload.model_dump())
    return success_response(PlayerAvailabilityRead.model_validate(record).model_dump(), "Availability record created")


@router.put("/{availability_id}", response_model=dict)
def update_availability(availability_id: int, payload: PlayerAvailabilityUpdate, db: Session = Depends(get_db)):
    record = PlayerAvailabilityService(db).update_availability(availability_id, payload.model_dump(exclude_unset=True))
    return success_response(PlayerAvailabilityRead.model_validate(record).model_dump(), "Availability record updated")


@router.delete("/{availability_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_availability(availability_id: int, db: Session = Depends(get_db)):
    PlayerAvailabilityService(db).delete_availability(availability_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)