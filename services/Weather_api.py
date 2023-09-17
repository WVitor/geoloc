from os import getenv as env
import requests as req
from datetime import datetime, timedelta


class Weather_api:
    url: str
    key: str

    def __init__(self):
        self.url = "http://api.weatherapi.com/v1/"
        self.key = env("WEATHER_KEY")

    def get_current(self, city: str, aqi: str = "yes"):
        url = f"{self.url}current.json?key={self.key}&q={city}&aqi={aqi}"
        response = req.get(url)
        return response.json()

    def get_forecast(self, city: str, days: int = 1, aqi: str = "yes", alerts: str = "yes" ):
        url = f"{self.url}forecast.json?key={self.key}&q={city}&days={days}&aqi={aqi}&alerts={alerts}"
        response = req.get(url)
        return response.json()
    
    def get_search(self, city: str):
        url = f"{self.url}search.json?key={self.key}&q={city}"
        response = req.get(url)
        return response.json()
    
    def get_history(self, city: str):
        data = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        url = f"{self.url}history.json?key={self.key}&q={city}&dt={data}"
        response = req.get(url)
        return response.json()
    
    def get_future(self, city: str):
        data = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        print(data)
        url = f"{self.url}future.json?key={self.key}&q={city}&dt={data}"
        response = req.get(url)
        return response.json()
    
    def get_astronomy(self, city: str):
        data = datetime.now().strftime("%Y-%m-%d")
        url = f"{self.url}astronomy.json?key={self.key}&q={city}&dt={data}"
        response = req.get(url)
        return response.json()
    
    def get_time_zone(self, city: str):
        url = f"{self.url}timezone.json?key={self.key}&q={city}"
        response = req.get(url)
        return response.json()