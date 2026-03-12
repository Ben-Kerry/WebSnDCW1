TEAM_ALIASES = {
    "Man United": "Manchester United",
    "Inter Milan": "Inter",
}


def normalize_team_name(name: str) -> str:
    return TEAM_ALIASES.get(name.strip(), name.strip())


def normalize_player_name(name: str) -> str:
    return " ".join(name.split()).strip()