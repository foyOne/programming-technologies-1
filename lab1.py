import requests
from sqlalchemy import create_engine, Table, Column, String, Float, MetaData
from sqlalchemy.sql import select
from Database import Database as DB


class WeatherProvider:
    def __init__(self, key):
        self.key = key

    def get_data(self, location, start_date, end_date):
        url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history'
        params = {
            'aggregateHours': 24,
            'startDateTime': f'{start_date}T00:0:00',
            'endDateTime': f'{end_date}T23:59:59',
            'unitGroup': 'metric',
            'location': location,
            'key': self.key,
            'contentType': 'json',
        }
        data = requests.get(url, params).json()
        return [
            {
                'date': row['datetimeStr'][:10],
                'mint': row['mint'],
                'maxt': row['maxt'],
                'location': 'Volgograd,Russia',
                'humidity': row['humidity'],
            }
            for row in data['locations'][location]['values']
        ]

db = DB('sqlite:///weather.sqlite3')
db.AddTable("weather", date=str, mint=float, maxt=float, location=str, humidity=float)
db.Create()

provider = WeatherProvider('61GBF341EILPIA5A42W7VM2WK')
data = provider.get_data('Volgograd,Russia', '2020-09-20', '2020-09-29')

db.Insert("weather", data)
selectResult = db.Select("weather")

for row in selectResult:
    print(row)
