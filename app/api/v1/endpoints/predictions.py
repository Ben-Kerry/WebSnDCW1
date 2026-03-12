from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.prediction import generate_predictions

router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.post("/generate")
def generate(db: Session = Depends(get_db)):
    preds = generate_predictions(db)

    return {
        "message": "Predictions generated",
        "count": len(preds),
    }