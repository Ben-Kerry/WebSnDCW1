def parse_matches(raw_rows: list[dict]) -> list[dict]:
    matches = []
    for row in raw_rows:
        matches.append(
            {
                "home_team_id": row["home_team_id"],
                "away_team_id": row["away_team_id"],
                "round_name": row["round_name"],
                "leg_number": row.get("leg_number"),
                "bracket_slot": row.get("bracket_slot"),
                "match_date": row["match_date"],
                "venue": row["venue"],
                "is_neutral_venue": row.get("is_neutral_venue", False),
                "home_score": row.get("home_score"),
                "away_score": row.get("away_score"),
                "status": row.get("status", "scheduled"),
                "winner_team_id": row.get("winner_team_id"),
            }
        )
    return matches