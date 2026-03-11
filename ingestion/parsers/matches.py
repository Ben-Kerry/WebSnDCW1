"""Matches parser placeholder."""

from typing import Iterable


def parse_matches(raw: Iterable[dict]) -> list[dict]:
    """Parse raw match payloads (placeholder)."""
    return [dict(item) for item in raw] if raw else []