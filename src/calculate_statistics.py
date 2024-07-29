from datetime import datetime
from sqlalchemy import func
from app import create_app
from extensions import db
from models import WeatherData, WeatherStatistics

def calculate_statistics():
    # Create a Flask application context
    app = create_app()
    with app.app_context():
        # Get distinct station IDs from the WeatherData table
        stations = db.session.query(WeatherData.station_id).distinct()
        for station in stations:
            station_id = station[0]
            # Get distinct years for the current station
            years = db.session.query(func.extract('year', WeatherData.date).distinct()).filter_by(station_id=station_id).all()
            for year in years:
                year = int(year[0])
                # Calculate average maximum temperature for the current station and year, ignoring None values
                avg_max_temp = db.session.query(func.avg(WeatherData.max_temp)).filter(
                    WeatherData.station_id == station_id,
                    func.extract('year', WeatherData.date) == year,
                    WeatherData.max_temp != None
                ).scalar()
                # Calculate average minimum temperature for the current station and year, ignoring None values
                avg_min_temp = db.session.query(func.avg(WeatherData.min_temp)).filter(
                    WeatherData.station_id == station_id,
                    func.extract('year', WeatherData.date) == year,
                    WeatherData.min_temp != None
                ).scalar()
                # Calculate total precipitation for the current station and year, ignoring None values
                total_precipitation = db.session.query(func.sum(WeatherData.precipitation)).filter(
                    WeatherData.station_id == station_id,
                    func.extract('year', WeatherData.date) == year,
                    WeatherData.precipitation != None
                ).scalar()

                # Store the calculated statistics in the WeatherStatistics table
                weather_stats = WeatherStatistics(
                    station_id=station_id,
                    year=year,
                    avg_max_temp=avg_max_temp,
                    avg_min_temp=avg_min_temp,
                    total_precipitation=total_precipitation
                )
                db.session.add(weather_stats)
        # Commit the transaction to save the statistics in the database
        db.session.commit()
        print("Weather statistics calculated and stored successfully")

if __name__ == '__main__':
    calculate_statistics()