from sqlalchemy.orm import Session

from app.models.probability import Probability


class ProbabilityRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Probability]:
        return self.db.query(Probability).order_by(Probability.win_probability.desc()).all()

    def get(self, probability_id: int) -> Probability | None:
        return self.db.query(Probability).filter(Probability.id == probability_id).first()

    def create(self, payload: dict) -> Probability:
        probability = Probability(**payload)
        self.db.add(probability)
        self.db.commit()
        self.db.refresh(probability)
        return probability

    def update(self, probability: Probability, payload: dict) -> Probability:
        for key, value in payload.items():
            setattr(probability, key, value)
        self.db.commit()
        self.db.refresh(probability)
        return probability

    def delete(self, probability: Probability) -> None:
        self.db.delete(probability)
        self.db.commit()