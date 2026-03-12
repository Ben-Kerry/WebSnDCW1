from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.match import MatchRepository
from app.repositories.match_prediction import MatchPredictionRepository


class MatchPredictionService:
    def __init__(self, db: Session):
        self.repo = MatchPredictionRepository(db)
        self.match_repo = MatchRepository(db)

    def list_predictions(self):
        return self.repo.list()

    def get_prediction(self, prediction_id: int):
        prediction = self.repo.get(prediction_id)
        if not prediction:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match prediction not found")
        return prediction

    def create_prediction(self, payload: dict):
        if not self.match_repo.get(payload["match_id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid match_id")
        return self.repo.create(payload)

    def update_prediction(self, prediction_id: int, payload: dict):
        prediction = self.get_prediction(prediction_id)
        if "match_id" in payload and not self.match_repo.get(payload["match_id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid match_id")
        return self.repo.update(prediction, payload)

    def delete_prediction(self, prediction_id: int):
        prediction = self.get_prediction(prediction_id)
        self.repo.delete(prediction)