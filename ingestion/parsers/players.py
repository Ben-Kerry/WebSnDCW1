"""Players parser placeholder."""

from typing import Iterable


def parse_players(raw: Iterable[dict]) -> list[dict]:
    """Parse raw player payloads (placeholder)."""
    return [dict(item) for item in raw] if raw else []