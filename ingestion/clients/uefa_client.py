"""UEFA API client placeholder."""

from typing import Any


class UEFAClient:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key

    def fetch_competitions(self) -> list[dict[str, Any]]:
        """Fetch competitions from UEFA (placeholder)."""
        return []