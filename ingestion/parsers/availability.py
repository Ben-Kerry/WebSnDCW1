def parse_availability(raw_rows: list[dict]) -> list[dict]:
    records = []
    for row in raw_rows:
        records.append(
            {
                "player_id": row["player_id"],
                "team_id": row["team_id"],
                "status": row["status"],
                "reason": row.get("reason"),
                "as_of_date": row["as_of_date"],
            }
        )
    return records