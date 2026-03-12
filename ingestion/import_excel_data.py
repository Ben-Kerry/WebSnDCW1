from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import requests

API_BASE = "http://localhost:8000/api/v1"
EXCEL_PATH = Path("data/europa_league_data.xlsx")


class ApiClient:
    def __init__(self, base_url: str = API_BASE) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def get(self, resource: str) -> dict[str, Any]:
        response = self.session.get(f"{self.base_url}/{resource}", timeout=30)
        response.raise_for_status()
        return response.json()

    def post(self, resource: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = self.session.post(f"{self.base_url}/{resource}", json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def close(self) -> None:
        self.session.close()


def clean_value(value: Any) -> Any:
    if pd.isna(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    return value


def row_to_dict(row: dict[str, Any]) -> dict[str, Any]:
    return {key: clean_value(value) for key, value in row.items()}


def read_sheet(path: Path, sheet_name: str) -> list[dict[str, Any]]:
    df = pd.read_excel(path, sheet_name=sheet_name)
    df = df.where(pd.notnull(df), None)
    return [row_to_dict(row) for row in df.to_dict(orient="records")]


def build_lookup(api: ApiClient, resource: str, key_field: str = "name") -> dict[str, int]:
    payload = api.get(resource)
    rows = payload["data"]
    return {row[key_field]: row["id"] for row in rows}


def safe_post(api: ApiClient, resource: str, payload: dict[str, Any]) -> None:
    try:
        api.post(resource, payload)
        print(f"Created {resource}: {payload}")
    except requests.HTTPError as exc:
        response = exc.response
        detail = response.text if response is not None else str(exc)
        print(f"Failed {resource}: {payload}")
        print(detail)


def import_teams(api: ApiClient, path: Path) -> None:
    rows = read_sheet(path, "teams")
    for row in rows:
        payload = {
            "name": row["name"],
            "country": row["country"],
            "coach": row.get("coach"),
            "founded_year": row.get("founded_year"),
            "uefa_coefficient": row.get("uefa_coefficient", 0.0) or 0.0,
        }
        safe_post(api, "teams", payload)


def import_players(api: ApiClient, path: Path) -> None:
    rows = read_sheet(path, "players")
    team_lookup = build_lookup(api, "teams")

    for row in rows:
        team_name = row["team_name"]
        team_id = team_lookup.get(team_name)

        if not team_id:
            print(f"Skipping player {row['name']}: unknown team '{team_name}'")
            continue

        payload = {
            "name": row["name"],
            "position": row["position"],
            "nationality": row["nationality"],
            "age": int(row["age"]),
            "goals": int(row.get("goals", 0) or 0),
            "assists": int(row.get("assists", 0) or 0),
            "rating": float(row.get("rating", 0.0) or 0.0),
            "team_id": team_id,
        }
        safe_post(api, "players", payload)


def import_matches(api: ApiClient, path: Path) -> None:
    rows = read_sheet(path, "matches")
    team_lookup = build_lookup(api, "teams")

    for row in rows:
        home_name = row["home_team"]
        away_name = row["away_team"]

        home_team_id = team_lookup.get(home_name)
        away_team_id = team_lookup.get(away_name)

        if not home_team_id or not away_team_id:
            print(f"Skipping match: unknown team mapping '{home_name}' vs '{away_name}'")
            continue

        payload = {
            "home_team_id": home_team_id,
            "away_team_id": away_team_id,
            "round_name": row["round_name"],
            "leg_number": int(row["leg_number"]) if row.get("leg_number") is not None else None,
            "bracket_slot": row.get("bracket_slot"),
            "match_date": row["match_date"],
            "venue": row["venue"],
            "is_neutral_venue": bool(row.get("is_neutral_venue", False)),
            "home_score": int(row["home_score"]) if row.get("home_score") is not None else None,
            "away_score": int(row["away_score"]) if row.get("away_score") is not None else None,
            "status": row.get("status", "scheduled") or "scheduled",
            "winner_team_id": None,
        }
        safe_post(api, "matches", payload)


def import_team_form(api: ApiClient, path: Path) -> None:
    rows = read_sheet(path, "team_form")
    team_lookup = build_lookup(api, "teams")

    for row in rows:
        team_name = row["team_name"]
        team_id = team_lookup.get(team_name)

        if not team_id:
            print(f"Skipping team form for '{team_name}': unknown team")
            continue

        payload = {
            "team_id": team_id,
            "as_of_date": row["as_of_date"],
            "last_5_wins": int(row.get("last_5_wins", 0) or 0),
            "last_5_draws": int(row.get("last_5_draws", 0) or 0),
            "last_5_losses": int(row.get("last_5_losses", 0) or 0),
            "last_5_goals_for": int(row.get("last_5_goals_for", 0) or 0),
            "last_5_goals_against": int(row.get("last_5_goals_against", 0) or 0),
            "home_form_rating": float(row.get("home_form_rating", 0.0) or 0.0),
            "away_form_rating": float(row.get("away_form_rating", 0.0) or 0.0),
        }
        safe_post(api, "team-form", payload)


def import_player_availability(api: ApiClient, path: Path) -> None:
    rows = read_sheet(path, "player_availability")
    team_lookup = build_lookup(api, "teams")
    player_lookup = build_lookup(api, "players")

    for row in rows:
        team_name = row["team_name"]
        player_name = row["player_name"]

        team_id = team_lookup.get(team_name)
        player_id = player_lookup.get(player_name)

        if not team_id:
            print(f"Skipping availability for '{player_name}': unknown team '{team_name}'")
            continue

        if not player_id:
            print(f"Skipping availability: unknown player '{player_name}'")
            continue

        payload = {
            "player_id": player_id,
            "team_id": team_id,
            "status": row["status"],
            "reason": row.get("reason"),
            "as_of_date": row["as_of_date"],
        }
        safe_post(api, "player-availability", payload)


def main() -> None:
    if not EXCEL_PATH.exists():
        raise FileNotFoundError(f"Excel file not found: {EXCEL_PATH}")

    api = ApiClient()
    try:
        print("Importing teams...")
        import_teams(api, EXCEL_PATH)

        if "players" in pd.ExcelFile(EXCEL_PATH).sheet_names:
            print("Importing players...")
            import_players(api, EXCEL_PATH)

        print("Importing matches...")
        import_matches(api, EXCEL_PATH)

        if "team_form" in pd.ExcelFile(EXCEL_PATH).sheet_names:
            print("Importing team form...")
            import_team_form(api, EXCEL_PATH)

        if "player_availability" in pd.ExcelFile(EXCEL_PATH).sheet_names:
            print("Importing player availability...")
            import_player_availability(api, EXCEL_PATH)

        print("Excel import complete.")
    finally:
        api.close()


if __name__ == "__main__":
    main()