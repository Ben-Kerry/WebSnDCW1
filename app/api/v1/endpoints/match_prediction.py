from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.match_prediction import MatchPredictionCreate, MatchPredictionRead, MatchPredictionUpdate
from app.services.match_prediction import MatchPredictionService
from app.utils.responses import success_response

router = APIRouter(prefix="/match-predictions", tags=["Match Predictions"])


@router.get("", response_model=dict)
def list_predictions(db: Session = Depends(get_db)):
    data = [MatchPredictionRead.model_validate(item).model_dump() for item in MatchPredictionService(db).list_predictions()]
    return success_response(data, "Match predictions retrieved")


@router.get("/{prediction_id}", response_model=dict)
def get_prediction(prediction_id: int, db: Session = Depends(get_db)):
    prediction = MatchPredictionService(db).get_prediction(prediction_id)
    return success_response(MatchPredictionRead.model_validate(prediction).model_dump(), "Match prediction retrieved")


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_prediction(payload: MatchPredictionCreate, db: Session = Depends(get_db)):
    prediction = MatchPredictionService(db).create_prediction(payload.model_dump())
    return success_response(MatchPredictionRead.model_validate(prediction).model_dump(), "Match prediction created")


@router.put("/{prediction_id}", response_model=dict)
def update_prediction(prediction_id: int, payload: MatchPredictionUpdate, db: Session = Depends(get_db)):
    prediction = MatchPredictionService(db).update_prediction(prediction_id, payload.model_dump(exclude_unset=True))
    return success_response(MatchPredictionRead.model_validate(prediction).model_dump(), "Match prediction updated")


@router.delete("/{prediction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prediction(prediction_id: int, db: Session = Depends(get_db)):
    MatchPredictionService(db).delete_prediction(prediction_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)