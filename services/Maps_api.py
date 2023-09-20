from os import getenv as env
import requests as req
from datetime import datetime, timedelta


class Maps_api:
    url: str
    key: str

    def __init__(self):
        self.url = "https://maps.googleapis.com/maps/api"
        self.key = env("MAPS_KEY")

    def get_places(self, location: str, radius: int = 2000, type: str = "restaurant"):
        params = {
            "location": location,
            "radius": radius,
            "keyword": type,
            "key": self.key
        }
        url = f"{self.url}/place/nearbysearch/json?"
        response = req.get(url, params)
        return response.json()