import requests
import time
from datetime import datetime


class VisualCrossing:
    
    def __init__(self):
        self.Key = "61GBF341EILPIA5A42W7VM2WK"
    
    def Get(self, Location, StartDate, EndDate):
        URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history"
        Params = {
            'aggregateHours': 24,
            'startDateTime': f'{StartDate}T00:0:00',
            'endDateTime': f'{EndDate}T23:59:59',
            'unitGroup': 'metric',
            'location': Location,
            'key': self.Key,
            'contentType': 'json',
        }
        Data = requests.get(URL, Params).json()
        return [
            {
                "date": row["datetimeStr"][:10],
                "mint": row["mint"],
                "maxt": row["maxt"],
                "location": Location,
                "humidity": row["humidity"],
            }
            for row in Data["locations"][Location]["values"]
        ]


class OpenWeather:

    def __init__(self):
        self.Key = "3d6ddedc97ac5c897a4da33d42f8b492"
    
    def Get(self, Location):
        URL = "http://api.openweathermap.org/data/2.5/weather"
        Params = {
            "units": "metric",
            "q": Location,
            "appid": self.Key,
        }
        Data = requests.get(URL, Params).json()
        return {
            "date": datetime.fromtimestamp(Data["dt"]).strftime("%Y-%m-%d %H:%M:%S"),
            "mint": Data["main"]["temp_min"],
            "maxt": Data["main"]["temp_max"],
            "location": Location,
            "humidity": Data["main"]["humidity"],
        }