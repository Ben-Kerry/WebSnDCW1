from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.tournament_simulation import (
    simulate_tournament_many,
    simulate_tournament_once,
)

router = APIRouter(prefix="/tournament", tags=["Tournament Simulation"])


@router.get("/simulate-once", response_model=dict)
def simulate_once(db: Session = Depends(get_db)):
    return {
        "success": True,
        "data": simulate_tournament_once(db),
    }


@router.get("/simulate-many", response_model=dict)
def simulate_many(
    runs: int = Query(default=1000, ge=1, le=100000),
    db: Session = Depends(get_db),
):
    return {
        "success": True,
        "data": simulate_tournament_many(db, runs=runs),
    }