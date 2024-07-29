import os
import logging
from datetime import datetime
from app import create_app
from extensions import db
from models import WeatherData

# Configure logging to output information at the INFO level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Directory where weather data files are located
DATA_DIR = 'D:\\Corteva\\corteva\\weather-data-pipeline-api\\wx_data'

def parse_line(line):
    """
    Parses a line from the weather data file.

    Args:
        line (str): A line from the weather data file.

    Returns:
        tuple: A tuple containing the date, maximum temperature, minimum temperature,
               and precipitation, with appropriate conversions and handling of missing values.
    """
    date_str, max_temp, min_temp, precipitation = line.strip().split('\t')
    date = datetime.strptime(date_str, '%Y%m%d').date()  # Convert date string to date object
    max_temp = int(max_temp) / 10 if int(max_temp) != -9999 else None  # Convert max_temp to degrees Celsius, handle missing value
    min_temp = int(min_temp) / 10 if int(min_temp) != -9999 else None  # Convert min_temp to degrees Celsius, handle missing value
    precipitation = int(precipitation) / 10 if int(precipitation) != -9999 else None  # Convert precipitation to centimeters, handle missing value
    return date, max_temp, min_temp, precipitation

def ingest_weather_data():
    """
    Ingests weather data from files into the database.

    The function performs the following tasks:
    - Initializes the Flask application and database context.
    - Iterates through all files in the data directory.
    - Parses each line of the files and processes records.
    - Checks for duplicates to avoid inserting existing records.
    - Logs the duration of the ingestion process and the number of records ingested.
    """
    app = create_app()  # Create the Flask application instance
    with app.app_context():  # Ensure that the application context is available
        total_records = 0  # Counter for the total number of records ingested
        duplicate_records = 0  # Counter for the number of duplicate records found
        start_time = datetime.now()  # Record the start time of the ingestion process
        logger.info(f"Data ingestion started at {start_time}")

        # Loop through all files in the specified directory
        for filename in os.listdir(DATA_DIR):
            station_id = filename.split('.')[0]  # Extract station_id from filename
            with open(os.path.join(DATA_DIR, filename), 'r') as file:
                for line in file:
                    date, max_temp, min_temp, precipitation = parse_line(line)
                    
                    # Check if a record with the same station_id and date already exists
                    existing_record = WeatherData.query.filter_by(station_id=station_id, date=date).first()
                    if existing_record:
                        duplicate_records += 1  # Increment the duplicate record counter
                        continue  # Skip the existing record

                    # Create a new WeatherData instance and add it to the session
                    weather_data = WeatherData(
                        station_id=station_id,
                        date=date,
                        max_temp=max_temp,
                        min_temp=min_temp,
                        precipitation=precipitation
                    )
                    db.session.add(weather_data)  # Add the new record to the database session
                    total_records += 1  # Increment the total record counter

                # Commit the session to persist all changes to the database
                db.session.commit()
        
        end_time = datetime.now()  # Record the end time of the ingestion process
        logger.info(f"Data ingestion completed at {end_time}")
        logger.info(f"Total Duration: {end_time - start_time}")  # Log the total duration of the ingestion process
        logger.info(f"Total records ingested: {total_records}")  # Log the total number of records ingested
        logger.info(f"Total duplicate records found: {duplicate_records}")  # Log the total number of duplicate records found

if __name__ == '__main__':
    ingest_weather_data()  # Run the data ingestion process if this script is executed directly
