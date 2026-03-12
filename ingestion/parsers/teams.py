def parse_teams(raw_rows: list[dict]) -> list[dict]:
    teams = []
    for row in raw_rows:
        teams.append(
            {
                "name": row.get("name", "").strip(),
                "country": row.get("country", "").strip(),
                "coach": row.get("coach"),
                "founded_year": row.get("founded_year"),
                "uefa_coefficient": row.get("uefa_coefficient", 0.0),
            }
        )
    return teams