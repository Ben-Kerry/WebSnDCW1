from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.match import Match
from app.models.team_form import TeamForm
from app.models.match_prediction import MatchPrediction


HOME_ADVANTAGE = 0.3


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

    total = home_strength + away_strength

    home_win_prob = home_strength / total
    away_win_prob = away_strength / total
    draw_prob = 1 - (home_win_prob + away_win_prob) * 0.85

    prediction = MatchPrediction(
        match_id=match.id,
        home_win_probability=round(home_win_prob, 3),
        draw_probability=round(draw_prob, 3),
        away_win_probability=round(away_win_prob, 3),
        predicted_home_score=round(home_strength / 2),
        predicted_away_score=round(away_strength / 2),
    )

    return prediction


def generate_predictions(db: Session):
    matches = db.query(Match).all()

    predictions = []

    for match in matches:
        prediction = predict_match(db, match)

        if prediction:
            db.add(prediction)
            predictions.append(prediction)

    db.commit()

    return predictions