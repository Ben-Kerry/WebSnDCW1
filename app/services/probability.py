from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.probability import ProbabilityRepository
from app.repositories.team import TeamRepository


class ProbabilityService:
    def __init__(self, db: Session):
        self.repo = ProbabilityRepository(db)
        self.team_repo = TeamRepository(db)

    def list_probabilities(self):
        return self.repo.list()

    def get_probability(self, probability_id: int):
        probability = self.repo.get(probability_id)
        if not probability:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Probability record not found")
        return probability

    def create_probability(self, payload: dict):
        if not self.team_repo.get(payload["team_id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid team_id")
        return self.repo.create(payload)

    def update_probability(self, probability_id: int, payload: dict):
        probability = self.get_probability(probability_id)
        if "team_id" in payload and not self.team_repo.get(payload["team_id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid team_id")
        return self.repo.update(probability, payload)

    def delete_probability(self, probability_id: int):
        probability = self.get_probability(probability_id)
        self.repo.delete(probability)