from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.probability import ProbabilityCreate, ProbabilityRead, ProbabilityUpdate
from app.services.probability import ProbabilityService
from app.utils.responses import success_response

router = APIRouter(prefix="/probabilities", tags=["Probabilities"])


@router.get("", response_model=dict)
def list_probabilities(db: Session = Depends(get_db)):
    data = [ProbabilityRead.model_validate(item).model_dump() for item in ProbabilityService(db).list_probabilities()]
    return success_response(data, "Probabilities retrieved")


@router.get("/{probability_id}", response_model=dict)
def get_probability(probability_id: int, db: Session = Depends(get_db)):
    probability = ProbabilityService(db).get_probability(probability_id)
    return success_response(ProbabilityRead.model_validate(probability).model_dump(), "Probability retrieved")


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_probability(payload: ProbabilityCreate, db: Session = Depends(get_db)):
    probability = ProbabilityService(db).create_probability(payload.model_dump())
    return success_response(ProbabilityRead.model_validate(probability).model_dump(), "Probability created")


@router.put("/{probability_id}", response_model=dict)
def update_probability(probability_id: int, payload: ProbabilityUpdate, db: Session = Depends(get_db)):
    probability = ProbabilityService(db).update_probability(probability_id, payload.model_dump(exclude_unset=True))
    return success_response(ProbabilityRead.model_validate(probability).model_dump(), "Probability updated")


@router.delete("/{probability_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_probability(probability_id: int, db: Session = Depends(get_db)):
    ProbabilityService(db).delete_probability(probability_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)