from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.analytics import AnalyticsService
from app.utils.responses import success_response

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/leaderboard", response_model=dict)
def leaderboard(db: Session = Depends(get_db)):
    return success_response(AnalyticsService(db).leaderboard(), "Leaderboard generated")


@router.get("/players/summary", response_model=dict)
def player_summary(db: Session = Depends(get_db)):
    return success_response(AnalyticsService(db).player_summaries(), "Player summaries generated")


@router.get("/predictions/summary", response_model=dict)
def prediction_summary(db: Session = Depends(get_db)):
    return success_response(
        AnalyticsService(db).prediction_summaries(),
        "Prediction summaries generated",
    )