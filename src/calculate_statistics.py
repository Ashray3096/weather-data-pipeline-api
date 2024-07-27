# calculate_statistics.py
from datetime import datetime
from sqlalchemy import func
from app import create_app
from extensions import db
from models import WeatherData, WeatherStatistics

def calculate_statistics():
    app = create_app()
    with app.app_context():
        # Get distinct station IDs and years
        stations = db.session.query(WeatherData.station_id).distinct()
        for station in stations:
            station_id = station[0]
            years = db.session.query(func.extract('year', WeatherData.date).distinct()).filter_by(station_id=station_id).all()
            for year in years:
                year = int(year[0])
                # Calculate statistics
                avg_max_temp = db.session.query(func.avg(WeatherData.max_temp)).filter(
                    WeatherData.station_id == station_id,
                    func.extract('year', WeatherData.date) == year,
                    WeatherData.max_temp != None
                ).scalar()
                avg_min_temp = db.session.query(func.avg(WeatherData.min_temp)).filter(
                    WeatherData.station_id == station_id,
                    func.extract('year', WeatherData.date) == year,
                    WeatherData.min_temp != None
                ).scalar()
                total_precipitation = db.session.query(func.sum(WeatherData.precipitation)).filter(
                    WeatherData.station_id == station_id,
                    func.extract('year', WeatherData.date) == year,
                    WeatherData.precipitation != None
                ).scalar()

                # Convert precipitation to centimeters
                if total_precipitation is not None:
                    total_precipitation /= 10

                # Store the statistics
                weather_stats = WeatherStatistics(
                    station_id=station_id,
                    year=year,
                    avg_max_temp=avg_max_temp,
                    avg_min_temp=avg_min_temp,
                    total_precipitation=total_precipitation
                )
                db.session.add(weather_stats)
        db.session.commit()
        print("Weather statistics calculated and stored successfully")

if __name__ == '__main__':
    calculate_statistics()
