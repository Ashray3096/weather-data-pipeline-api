import os
from datetime import datetime
from app import create_app
from extensions import db
from models import WeatherData

DATA_DIR = 'D:\Corteva\corteva\weather-data-pipeline-api\wx_data'

def parse_line(line):
    date_str, max_temp, min_temp, precipitation = line.strip().split('\t')
    date = datetime.strptime(date_str, '%Y%m%d').date()
    max_temp = int(max_temp) if int(max_temp) != -9999 else None
    min_temp = int(min_temp) if int(min_temp) != -9999 else None
    precipitation = int(precipitation) if int(precipitation) != -9999 else None
    return date, max_temp, min_temp, precipitation

def ingest_weather_data():
    app = create_app()
    with app.app_context():
        for filename in os.listdir(DATA_DIR):
            station_id = filename.split('.')[0]
            with open(os.path.join(DATA_DIR, filename), 'r') as file:
                for line in file:
                    date, max_temp, min_temp, precipitation = parse_line(line)
                    weather_data = WeatherData(
                        station_id=station_id,
                        date=date,
                        max_temp=max_temp,
                        min_temp=min_temp,
                        precipitation=precipitation
                    )
                    db.session.add(weather_data)
                db.session.commit()
        print("Weather data ingested successfully")

if __name__ == '__main__':
    ingest_weather_data()
