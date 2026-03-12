from __future__ import annotations

from datetime import datetime, UTC

from sqlalchemy.orm import Session

from app.models.match import Match
from app.models.match_prediction import MatchPrediction
from app.models.team_form import TeamForm


HOME_ADVANTAGE = 0.3
MODEL_NAME = "form_based_model"
MODEL_VERSION = "1.0.0"


def predict_match(db: Session, match: Match) -> MatchPrediction | None:
    """Generate a prediction for a single match."""

    home_form = (
        db.query(TeamForm)
        .filter(TeamForm.team_id == match.home_team_id)
        .order_by(TeamForm.as_of_date.desc())
        .first()
    )

    away_form = (
        db.query(TeamForm)
        .filter(TeamForm.team_id == match.away_team_id)
        .order_by(TeamForm.as_of_date.desc())
        .first()
    )

    if not home_form or not away_form:
        return None

    home_strength = home_form.home_form_rating + HOME_ADVANTAGE
    away_strength = away_form.away_form_rating

    total_strength = home_strength + away_strength
    if total_strength <= 0:
        return None

    base_home = home_strength / total_strength
    base_away = away_strength / total_strength

    draw_probability = 0.24
    remaining = 1.0 - draw_probability

    home_win_probability = base_home * remaining
    away_win_probability = base_away * remaining

    predicted_home_goals = round(home_strength / 2, 2)
    predicted_away_goals = round(away_strength / 2, 2)

    confidence_gap = abs(home_win_probability - away_win_probability)
    confidence_score = round(min(1.0, 0.5 + confidence_gap), 3)

    prediction = MatchPrediction(
        match_id=match.id,
        model_name=MODEL_NAME,
        model_version=MODEL_VERSION,
        generated_at=datetime.now(UTC),
        home_win_probability=round(home_win_probability, 3),
        draw_probability=round(draw_probability, 3),
        away_win_probability=round(away_win_probability, 3),
        predicted_home_goals=predicted_home_goals,
        predicted_away_goals=predicted_away_goals,
        confidence_score=confidence_score,
    )

    return prediction


def generate_predictions(db: Session) -> list[MatchPrediction]:
    matches = db.query(Match).all()
    predictions: list[MatchPrediction] = []

    for match in matches:
        existing_prediction = (
            db.query(MatchPrediction)
            .filter(MatchPrediction.match_id == match.id)
            .first()
        )

        if existing_prediction:
            continue

        prediction = predict_match(db, match)

        if prediction:
            db.add(prediction)
            predictions.append(prediction)

    db.commit()
    return predictions