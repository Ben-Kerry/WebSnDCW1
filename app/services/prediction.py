from __future__ import annotations

from datetime import UTC, datetime
from math import exp, factorial

from sqlalchemy.orm import Session

from app.models.match import Match
from app.models.match_prediction import MatchPrediction
from app.models.team_form import TeamForm


HOME_ADVANTAGE = 0.25
MODEL_NAME = "poisson_form_model"
MODEL_VERSION = "1.0.0"
MAX_GOALS = 6


def poisson_pmf(k: int, lam: float) -> float:
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    return (exp(-lam) * (lam**k)) / factorial(k)


def expected_goals(home_form: TeamForm, away_form: TeamForm) -> tuple[float, float]:
    home_attack = max(0.2, home_form.last_5_goals_for / 5)
    home_defense = max(0.2, home_form.last_5_goals_against / 5)

    away_attack = max(0.2, away_form.last_5_goals_for / 5)
    away_defense = max(0.2, away_form.last_5_goals_against / 5)

    home_rating_factor = max(0.6, home_form.home_form_rating / 7.0)
    away_rating_factor = max(0.6, away_form.away_form_rating / 7.0)

    home_lambda = ((home_attack + away_defense) / 2) * home_rating_factor + HOME_ADVANTAGE
    away_lambda = ((away_attack + home_defense) / 2) * away_rating_factor

    return round(home_lambda, 3), round(away_lambda, 3)


def outcome_probabilities(home_lambda: float, away_lambda: float) -> tuple[float, float, float]:
    home_win = 0.0
    draw = 0.0
    away_win = 0.0

    for home_goals in range(MAX_GOALS + 1):
        for away_goals in range(MAX_GOALS + 1):
            prob = poisson_pmf(home_goals, home_lambda) * poisson_pmf(away_goals, away_lambda)

            if home_goals > away_goals:
                home_win += prob
            elif home_goals == away_goals:
                draw += prob
            else:
                away_win += prob

    total = home_win + draw + away_win
    if total > 0:
        home_win /= total
        draw /= total
        away_win /= total

    return round(home_win, 3), round(draw, 3), round(away_win, 3)


def confidence_score(home_win: float, draw: float, away_win: float) -> float:
    strongest = max(home_win, draw, away_win)
    return round(strongest, 3)


def predict_match(db: Session, match: Match) -> MatchPrediction | None:
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

    home_lambda, away_lambda = expected_goals(home_form, away_form)
    home_win, draw, away_win = outcome_probabilities(home_lambda, away_lambda)

    return MatchPrediction(
        match_id=match.id,
        model_name=MODEL_NAME,
        model_version=MODEL_VERSION,
        generated_at=datetime.now(UTC),
        home_win_probability=home_win,
        draw_probability=draw,
        away_win_probability=away_win,
        predicted_home_goals=round(home_lambda, 2),
        predicted_away_goals=round(away_lambda, 2),
        confidence_score=confidence_score(home_win, draw, away_win),
    )


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