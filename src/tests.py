import unittest
from app import create_app
from extensions import db
from models import WeatherData, WeatherStatistics

class ApiTestCase(unittest.TestCase):
    
    def setUp(self):
        # Create a new app instance for testing
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()  # Push the application context
        
        # Set up the database
        with self.app.app_context():
            db.create_all()
            self.populate_data()

    def tearDown(self):
        # Clean up database
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            self.app_context.pop()  # Pop the application context

    def populate_data(self):
        # Populate test data in the database
        weather_data = [
            WeatherData(station_id='USC001', date='2023-01-01', max_temp=10.0, min_temp=5.0, precipitation=1.0),
            WeatherData(station_id='USC001', date='2023-01-02', max_temp=11.0, min_temp=5.5, precipitation=1.5),
        ]
        weather_stats = [
            WeatherStatistics(station_id='USC001', year=2023, avg_max_temp=10.5, avg_min_temp=5.25, total_precipitation=1.25),
        ]
        with self.app.app_context():
            db.session.bulk_save_objects(weather_data)
            db.session.bulk_save_objects(weather_stats)
            db.session.commit()

    def test_get_weather(self):
        # Test the GET /api/weather endpoint
        response = self.app.test_client().get('/api/weather')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

    def test_get_weather_with_filters(self):
        # Test the GET /api/weather endpoint with filters
        response = self.app.test_client().get('/api/weather?station_id=USC001&start_date=2023-01-01&end_date=2023-01-01')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_get_weather_stats(self):
        # Test the GET /api/weather/stats endpoint
        response = self.app.test_client().get('/api/weather/stats')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_get_weather_stats_with_filters(self):
        # Test the GET /api/weather/stats endpoint with filters
        response = self.app.test_client().get('/api/weather/stats?station_id=USC001&year=2023')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

if __name__ == '__main__':
    unittest.main()