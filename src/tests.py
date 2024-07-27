import unittest
from app import app, db
from models import WeatherData, WeatherStatistics

class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        self.populate_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def populate_data(self):
        weather_data = [
            WeatherData(station_id='USC001', date='2023-01-01', max_temp=100, min_temp=50, precipitation=10),
            WeatherData(station_id='USC001', date='2023-01-02', max_temp=110, min_temp=55, precipitation=15),
        ]
        weather_stats = [
            WeatherStatistics(station_id='USC001', year=2023, avg_max_temp=10.0, avg_min_temp=5.0, total_precipitation=1.0),
        ]
        db.session.bulk_save_objects(weather_data)
        db.session.bulk_save_objects(weather_stats)
        db.session.commit()

    def test_get_weather(self):
        response = self.app.get('/api/weather')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

    def test_get_weather_with_filters(self):
        response = self.app.get('/api/weather?station_id=USC001&start_date=2023-01-01&end_date=2023-01-01')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_get_weather_stats(self):
        response = self.app.get('/api/weather/stats')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_get_weather_stats_with_filters(self):
        response = self.app.get('/api/weather/stats?station_id=USC001&year=2023')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

if __name__ == '__main__':
    unittest.main()
