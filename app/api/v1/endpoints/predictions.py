from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.prediction import generate_predictions

router = APIRouter(prefix="/predictions", tags=["Predictions"])


@router.post("/generate", response_model=dict)
def generate(db: Session = Depends(get_db)):
    predictions = generate_predictions(db)
    return {
        "success": True,
        "message": "Predictions generated",
        "count": len(predictions),
    }