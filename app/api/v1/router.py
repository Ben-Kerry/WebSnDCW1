from fastapi import APIRouter

from app.api.v1.endpoints.analytics import router as analytics_router
from app.api.v1.endpoints.matches import router as matches_router
from app.api.v1.endpoints.players import router as players_router
from app.api.v1.endpoints.probabilities import router as probabilities_router
from app.api.v1.endpoints.teams import router as teams_router

api_router = APIRouter()
api_router.include_router(teams_router)
api_router.include_router(players_router)
api_router.include_router(matches_router)
api_router.include_router(probabilities_router)
api_router.include_router(analytics_router)