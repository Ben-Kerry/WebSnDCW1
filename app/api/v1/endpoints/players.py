from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.player import PlayerCreate, PlayerRead, PlayerUpdate
from app.services.player import PlayerService
from app.utils.responses import success_response

router = APIRouter(prefix="/players", tags=["Players"])


@router.get("", response_model=dict)
def list_players(db: Session = Depends(get_db)):
    data = [PlayerRead.model_validate(player).model_dump() for player in PlayerService(db).list_players()]
    return success_response(data, "Players retrieved")


@router.get("/{player_id}", response_model=dict)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = PlayerService(db).get_player(player_id)
    return success_response(PlayerRead.model_validate(player).model_dump(), "Player retrieved")


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_player(payload: PlayerCreate, db: Session = Depends(get_db)):
    player = PlayerService(db).create_player(payload.model_dump())
    return success_response(PlayerRead.model_validate(player).model_dump(), "Player created")


@router.put("/{player_id}", response_model=dict)
def update_player(player_id: int, payload: PlayerUpdate, db: Session = Depends(get_db)):
    player = PlayerService(db).update_player(player_id, payload.model_dump(exclude_unset=True))
    return success_response(PlayerRead.model_validate(player).model_dump(), "Player updated")


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_player(player_id: int, db: Session = Depends(get_db)):
    PlayerService(db).delete_player(player_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)