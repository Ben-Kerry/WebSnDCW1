from sqlalchemy.orm import Session

from app.models.match_prediction import MatchPrediction


class MatchPredictionRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[MatchPrediction]:
        return self.db.query(MatchPrediction).order_by(MatchPrediction.generated_at.desc()).all()

    def get(self, prediction_id: int) -> MatchPrediction | None:
        return self.db.query(MatchPrediction).filter(MatchPrediction.id == prediction_id).first()

    def create(self, payload: dict) -> MatchPrediction:
        prediction = MatchPrediction(**payload)
        self.db.add(prediction)
        self.db.commit()
        self.db.refresh(prediction)
        return prediction

    def update(self, prediction: MatchPrediction, payload: dict) -> MatchPrediction:
        for key, value in payload.items():
            setattr(prediction, key, value)
        self.db.commit()
        self.db.refresh(prediction)
        return prediction

    def delete(self, prediction: MatchPrediction) -> None:
        self.db.delete(prediction)
        self.db.commit()