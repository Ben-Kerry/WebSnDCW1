def parse_players(raw_rows: list[dict]) -> list[dict]:
    players = []
    for row in raw_rows:
        players.append(
            {
                "name": row.get("name", "").strip(),
                "position": row.get("position", "Unknown").strip(),
                "nationality": row.get("nationality", "Unknown").strip(),
                "age": row.get("age", 18),
                "goals": row.get("goals", 0),
                "assists": row.get("assists", 0),
                "rating": row.get("rating", 0.0),
                "team_id": row["team_id"],
            }
        )
    return players