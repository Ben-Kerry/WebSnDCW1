from fastapi import APIRouter

from app.api.v1.endpoints.analytics import router as analytics_router
from app.api.v1.endpoints.matches import router as matches_router
from app.api.v1.endpoints.match_prediction import router as match_prediction_router
from app.api.v1.endpoints.player_availability import router as player_availability_router
from app.api.v1.endpoints.players import router as players_router
from app.api.v1.endpoints.squad_membership import router as squad_membership_router
from app.api.v1.endpoints.team_form import router as team_form_router
from app.api.v1.endpoints.teams import router as teams_router

api_router = APIRouter()
api_router.include_router(teams_router)
api_router.include_router(players_router)
api_router.include_router(matches_router)
api_router.include_router(squad_membership_router)
api_router.include_router(player_availability_router)
api_router.include_router(team_form_router)
api_router.include_router(match_prediction_router)
api_router.include_router(analytics_router)