from __future__ import annotations

import random
from dataclasses import dataclass
from math import exp, factorial
from typing import Any

from sqlalchemy.orm import Session

from app.models.match import Match
from app.models.team import Team
from app.models.team_form import TeamForm


HOME_ADVANTAGE = 0.25
MAX_GOALS = 6


@dataclass
class SimulatedLeg:
    home_team_id: int
    away_team_id: int
    home_team: str
    away_team: str
    home_goals: int
    away_goals: int


@dataclass
class SimulatedTieResult:
    bracket_slot: str
    round_name: str
    first_leg: SimulatedLeg | None
    second_leg: SimulatedLeg | None
    winner_team_id: int
    winner_team_name: str


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


def sample_goals(lam: float, max_goals: int = MAX_GOALS) -> int:
    probs = [poisson_pmf(k, lam) for k in range(max_goals + 1)]
    total = sum(probs)
    if total <= 0:
        return 0

    normalized = [p / total for p in probs]
    r = random.random()
    cumulative = 0.0

    for goals, prob in enumerate(normalized):
        cumulative += prob
        if r <= cumulative:
            return goals

    return max_goals


def get_team_form(db: Session, team_id: int) -> TeamForm:
    form = (
        db.query(TeamForm)
        .filter(TeamForm.team_id == team_id)
        .order_by(TeamForm.as_of_date.desc())
        .first()
    )
    if not form:
        raise ValueError(f"No team form found for team_id={team_id}")
    return form


def get_team_name(db: Session, team_id: int) -> str:
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise ValueError(f"No team found for team_id={team_id}")
    return team.name


def simulate_single_match(db: Session, home_team_id: int, away_team_id: int) -> SimulatedLeg:
    home_form = get_team_form(db, home_team_id)
    away_form = get_team_form(db, away_team_id)

    home_lambda, away_lambda = expected_goals(home_form, away_form)

    home_goals = sample_goals(home_lambda)
    away_goals = sample_goals(away_lambda)

    return SimulatedLeg(
        home_team_id=home_team_id,
        away_team_id=away_team_id,
        home_team=get_team_name(db, home_team_id),
        away_team=get_team_name(db, away_team_id),
        home_goals=home_goals,
        away_goals=away_goals,
    )


def break_tie_randomly(db: Session, team_a_id: int, team_b_id: int) -> int:
    form_a = get_team_form(db, team_a_id)
    form_b = get_team_form(db, team_b_id)

    strength_a = form_a.home_form_rating + form_a.away_form_rating
    strength_b = form_b.home_form_rating + form_b.away_form_rating

    total = strength_a + strength_b
    if total <= 0:
        return random.choice([team_a_id, team_b_id])

    if random.random() < (strength_a / total):
        return team_a_id
    return team_b_id


def simulate_two_legged_tie(
    db: Session,
    team_a_id: int,
    team_b_id: int,
    bracket_slot: str,
    round_name: str,
) -> SimulatedTieResult:
    first_leg = simulate_single_match(db, team_a_id, team_b_id)
    second_leg = simulate_single_match(db, team_b_id, team_a_id)

    team_a_agg = first_leg.home_goals + second_leg.away_goals
    team_b_agg = first_leg.away_goals + second_leg.home_goals

    if team_a_agg > team_b_agg:
        winner_team_id = team_a_id
    elif team_b_agg > team_a_agg:
        winner_team_id = team_b_id
    else:
        winner_team_id = break_tie_randomly(db, team_a_id, team_b_id)

    return SimulatedTieResult(
        bracket_slot=bracket_slot,
        round_name=round_name,
        first_leg=first_leg,
        second_leg=second_leg,
        winner_team_id=winner_team_id,
        winner_team_name=get_team_name(db, winner_team_id),
    )


def simulate_final(db: Session, team_a_id: int, team_b_id: int) -> dict[str, Any]:
    final_match = simulate_single_match(db, team_a_id, team_b_id)

    if final_match.home_goals > final_match.away_goals:
        winner_team_id = team_a_id
    elif final_match.away_goals > final_match.home_goals:
        winner_team_id = team_b_id
    else:
        winner_team_id = break_tie_randomly(db, team_a_id, team_b_id)

    return {
        "match": {
            "home_team": final_match.home_team,
            "away_team": final_match.away_team,
            "home_goals": final_match.home_goals,
            "away_goals": final_match.away_goals,
        },
        "winner_team_id": winner_team_id,
        "winner_team_name": get_team_name(db, winner_team_id),
    }


def get_round_of_16_pairs(db: Session) -> list[tuple[str, int, int]]:
    matches = (
        db.query(Match)
        .filter(Match.round_name == "Round of 16")
        .order_by(Match.bracket_slot.asc(), Match.leg_number.asc())
        .all()
    )

    grouped: dict[str, list[Match]] = {}
    for match in matches:
        grouped.setdefault(match.bracket_slot, []).append(match)

    pairs: list[tuple[str, int, int]] = []
    for bracket_slot, legs in grouped.items():
        first_leg = sorted(legs, key=lambda m: (m.leg_number or 0))[0]
        pairs.append((bracket_slot, first_leg.home_team_id, first_leg.away_team_id))

    return sorted(pairs, key=lambda row: row[0])


def simulate_tournament_once(db: Session) -> dict[str, Any]:
    r16_pairs = get_round_of_16_pairs(db)

    if len(r16_pairs) != 8:
        raise ValueError("Expected exactly 8 Round of 16 ties in the database.")

    r16_results = []
    r16_winners: list[int] = []

    for bracket_slot, team_a_id, team_b_id in r16_pairs:
        result = simulate_two_legged_tie(
            db=db,
            team_a_id=team_a_id,
            team_b_id=team_b_id,
            bracket_slot=bracket_slot,
            round_name="Round of 16",
        )
        r16_results.append(result)
        r16_winners.append(result.winner_team_id)

    qf_pairs = [
        ("QF-1", r16_winners[0], r16_winners[1]),
        ("QF-2", r16_winners[2], r16_winners[3]),
        ("QF-3", r16_winners[4], r16_winners[5]),
        ("QF-4", r16_winners[6], r16_winners[7]),
    ]

    qf_results = []
    qf_winners: list[int] = []

    for bracket_slot, team_a_id, team_b_id in qf_pairs:
        result = simulate_two_legged_tie(
            db=db,
            team_a_id=team_a_id,
            team_b_id=team_b_id,
            bracket_slot=bracket_slot,
            round_name="Quarter-final",
        )
        qf_results.append(result)
        qf_winners.append(result.winner_team_id)

    sf_pairs = [
        ("SF-1", qf_winners[0], qf_winners[1]),
        ("SF-2", qf_winners[2], qf_winners[3]),
    ]

    sf_results = []
    sf_winners: list[int] = []

    for bracket_slot, team_a_id, team_b_id in sf_pairs:
        result = simulate_two_legged_tie(
            db=db,
            team_a_id=team_a_id,
            team_b_id=team_b_id,
            bracket_slot=bracket_slot,
            round_name="Semi-final",
        )
        sf_results.append(result)
        sf_winners.append(result.winner_team_id)

    final_result = simulate_final(db, sf_winners[0], sf_winners[1])

    return {
        "round_of_16": [_serialize_tie_result(r) for r in r16_results],
        "quarter_finals": [_serialize_tie_result(r) for r in qf_results],
        "semi_finals": [_serialize_tie_result(r) for r in sf_results],
        "final": final_result,
        "champion": final_result["winner_team_name"],
    }


def simulate_tournament_many(db: Session, runs: int = 1000) -> dict[str, Any]:
    champion_counts: dict[str, int] = {}

    for _ in range(runs):
        result = simulate_tournament_once(db)
        champion = result["champion"]
        champion_counts[champion] = champion_counts.get(champion, 0) + 1

    champion_probabilities = [
        {
            "team": team,
            "titles": count,
            "probability": round(count / runs, 4),
        }
        for team, count in sorted(champion_counts.items(), key=lambda item: item[1], reverse=True)
    ]

    return {
        "runs": runs,
        "champion_probabilities": champion_probabilities,
    }


def _serialize_tie_result(result: SimulatedTieResult) -> dict[str, Any]:
    return {
        "bracket_slot": result.bracket_slot,
        "round_name": result.round_name,
        "first_leg": {
            "home_team": result.first_leg.home_team if result.first_leg else None,
            "away_team": result.first_leg.away_team if result.first_leg else None,
            "home_goals": result.first_leg.home_goals if result.first_leg else None,
            "away_goals": result.first_leg.away_goals if result.first_leg else None,
        },
        "second_leg": {
            "home_team": result.second_leg.home_team if result.second_leg else None,
            "away_team": result.second_leg.away_team if result.second_leg else None,
            "home_goals": result.second_leg.home_goals if result.second_leg else None,
            "away_goals": result.second_leg.away_goals if result.second_leg else None,
        },
        "winner_team_id": result.winner_team_id,
        "winner_team_name": result.winner_team_name,
    }