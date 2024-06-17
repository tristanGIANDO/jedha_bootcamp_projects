import os
import requests
import pandas as pd
from dotenv import load_dotenv, find_dotenv
import envs

load_dotenv(find_dotenv("./.env"))

"""PATTERN
https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}
&exclude={part}&appid={API key}
"""


class WeatherData:
    def __init__(self, cities: list[str]) -> None:
        self._cities = cities

        # self._df = pd.DataFrame(["city", "lat", "lon"])
        # self._df = pd.DataFrame(self.get_cities_coordinates())
        self._df = pd.DataFrame(envs.COORD_BKP)

    def get_cities_coordinates(self):
        url = "https://nominatim.openstreetmap.org"
        endpoint = "search"
        data = []
        for city in self._cities:
            city = city.lower()
            payload = {"city": city, "format": "json"}
            response = requests.get(f"{url}/{endpoint}", params=payload)

            if response.status_code != 200:
                print(f"Failed with '{city}' -> {response.status_code}")
                continue

            resp = response.json()[0]
            data.append({"city": city,
                         "lat": resp.get("lat", None),
                         "lon": resp.get("lon", None)})

        return data

    def get_weather_data(self):
        url = "https://api.openweathermap.org/data/2.5"
        endpoint = "onecall"
        headers = {"appid": os.getenv("WEATHER_KEY")}

        for row in self._df.iterrows():
            payload = {"lat": row["lat"], "lon": row["lon"]}
            response = requests.get(f"{url}/{endpoint}",
                                    headers=headers,
                                    params=payload)

            if response.status_code != 200:
                print(f"Failed -> {response.status_code}")
                continue

            resp = response.json()[0]


if __name__ == "__main__":
    wd = WeatherData(envs.CITIES)
