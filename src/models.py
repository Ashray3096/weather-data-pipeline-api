from extensions import db

# Model representing weather data records
class WeatherData(db.Model):
    __tablename__ = 'weather_data'
    
    # Primary key for the table, auto-incremented
    id = db.Column(db.Integer, primary_key=True)
    
    # Station identifier, should be a string with a maximum length of 50 characters
    station_id = db.Column(db.String(50), nullable=False)
    
    # Date of the weather record, stored as a date object
    date = db.Column(db.Date, nullable=False)
    
    # Maximum temperature recorded for the day (in tenths of a degree Celsius)
    max_temp = db.Column(db.Integer)
    
    # Minimum temperature recorded for the day (in tenths of a degree Celsius)
    min_temp = db.Column(db.Integer)
    
    # Amount of precipitation for the day (in tenths of a millimeter)
    precipitation = db.Column(db.Integer)

# Model representing calculated weather statistics
class WeatherStatistics(db.Model):
    __tablename__ = 'weather_statistics'
    
    # Primary key for the table, auto-incremented
    id = db.Column(db.Integer, primary_key=True)
    
    # Station identifier, should be a string with a maximum length of 50 characters
    station_id = db.Column(db.String(50), nullable=False)
    
    # Year for which the statistics are calculated
    year = db.Column(db.Integer, nullable=False)
    
    # Average maximum temperature for the year (in degrees Celsius)
    avg_max_temp = db.Column(db.Float)
    
    # Average minimum temperature for the year (in degrees Celsius)
    avg_min_temp = db.Column(db.Float)
    
    # Total accumulated precipitation for the year (in centimeters)
    total_precipitation = db.Column(db.Float)