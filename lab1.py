import requests
from sqlalchemy import create_engine, Table, Column, String, Float, MetaData
from sqlalchemy.sql import select
from Database import Database as DB
from Providers import VisualCrossing


db = DB('sqlite:///weather.sqlite3')
db.AddTable("weather", date=str, mint=float, maxt=float, location=str, humidity=float)
db.Create()

provider = VisualCrossing()
data = provider.Get('Volgograd,Russia', '2020-09-20', '2020-09-29')

db.Insert("weather", data)
selectResult = db.Select("weather")

for row in selectResult:
    print(row)
