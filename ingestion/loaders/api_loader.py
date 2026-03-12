import requests


class ApiLoader:
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url.rstrip("/")

    def post(self, resource: str, payload: dict):
        response = requests.post(f"{self.base_url}/{resource}", json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def get(self, resource: str):
        response = requests.get(f"{self.base_url}/{resource}", timeout=30)
        response.raise_for_status()
        return response.json()