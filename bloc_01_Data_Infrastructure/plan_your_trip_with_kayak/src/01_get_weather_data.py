import os
import requests
import pandas as pd
from dotenv import load_dotenv, find_dotenv
import envs

load_dotenv(find_dotenv("./.env"))


class WeatherData:
    def __init__(self, cities: list[str]) -> None:
        self._cities = cities

        # self._data = pd.DataFrame(["city", "lat", "lon"])
        # self._data = pd.DataFrame(self.get_cities_coordinates())
        self._data = envs.COORD_BKP

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
        """
        list.dt = time UTC
        list.main.temp = temperature
        list.main.temp_min = temperature
        list.main.temp_max = temperature
        list.main.humidity = humidity
        list.pop = proba precipitation entre 0 et 1 (%)
        # list.rain.3h = volume de pluie (mm)
        list.clouds.all = cloudiness %
        """
        url = "https://api.openweathermap.org/data/2.5"
        endpoint = "forecast"
        data = []
        city_id = 1
        for row in self._data.copy():
            payload = {"lat": float(row["lat"]),
                       "lon": float(row["lon"]),
                       "units": "metric",
                       "cnt": 7,
                       "appid": os.getenv("WEATHER_KEY")}

            response = requests.get(f"{url}/{endpoint}",
                                    params=payload)

            if response.status_code != 200:
                print(f"Failed -> {response.status_code}")
                continue

            day_id = 1
            for dt in response.json()["list"]:
                data.append({
                    "city_id": city_id,
                    "city": row["city"],
                    "lat": float(row["lat"]),
                    "lon": float(row["lon"]),
                    "day_id": day_id,
                    "temp": dt["main"].get("temp", None),
                    "temp_min": dt["main"].get("temp_min", None),
                    "temp_max": dt["main"].get("temp_max", None),
                    "humidity": dt["main"].get("humidity", None),
                    "clouds": dt["clouds"].get("all", None),
                    "rain_prob": dt.get("pop", None),
                })
                day_id += 1
            city_id += 1

        return data


if __name__ == "__main__":
    wd = WeatherData(envs.CITIES)
    cities_gps = envs.COORD_BKP  # wd.get_cities_coordinates()
    weather_data = wd.get_weather_data()

    df = pd.DataFrame(weather_data)
    filename = os.path.join(
        os.path.dirname(__file__), "csv_files", "weather_data.csv")
    df.to_csv(filename, index=False, encoding="utf-8")
