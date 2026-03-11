"""Teams parser placeholder."""

from typing import Iterable


def parse_teams(raw: Iterable[dict]) -> list[dict]:
    """Parse raw team payloads into normalized dicts (placeholder)."""
    return [dict(item) for item in raw] if raw else []