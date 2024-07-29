import os
import logging
from datetime import datetime
from app import create_app
from extensions import db
from models import WeatherData

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_DIR = 'D:\\Corteva\\corteva\\weather-data-pipeline-api\\wx_data'

def parse_line(line):
    date_str, max_temp, min_temp, precipitation = line.strip().split('\t')
    date = datetime.strptime(date_str, '%Y%m%d').date()
    max_temp = int(max_temp) / 10 if int(max_temp) != -9999 else None
    min_temp = int(min_temp) / 10  if int(min_temp) != -9999 else None
    precipitation = int(precipitation) / 10 if int(precipitation) != -9999 else None
    return date, max_temp, min_temp, precipitation

def ingest_weather_data():
    app = create_app()
    with app.app_context():
        total_records = 0
        duplicate_records = 0
        start_time = datetime.now()
        logger.info(f"Data ingestion started at {start_time}")

        for filename in os.listdir(DATA_DIR):
            station_id = filename.split('.')[0]
            with open(os.path.join(DATA_DIR, filename), 'r') as file:
                for line in file:
                    date, max_temp, min_temp, precipitation = parse_line(line)
                    
                    # Check if the record already exists
                    existing_record = WeatherData.query.filter_by(station_id=station_id, date=date).first()
                    if existing_record:
                        duplicate_records += 1
                        continue

                    weather_data = WeatherData(
                        station_id=station_id,
                        date=date,
                        max_temp=max_temp,
                        min_temp=min_temp,
                        precipitation=precipitation
                    )
                    db.session.add(weather_data)
                    total_records += 1
                db.session.commit()
        
        end_time = datetime.now()
        logger.info(f"Data ingestion completed at {end_time}")
        logger.info(f"Total Duration: {end_time - start_time}")
        logger.info(f"Total records ingested: {total_records}")
        logger.info(f"Total duplicate records found: {duplicate_records}")

if __name__ == '__main__':
    ingest_weather_data()
