import unittest
from unittest.mock import patch, MagicMock
from tools.weather_tool import WeatherTool
from tools.air_quality_tool import AirQualityTool
import os
import requests

class TestWeatherTool(unittest.TestCase):
    def setUp(self):
        self.tool = WeatherTool()
        os.environ["OPENWEATHER_API_KEY"] = "test_key"

    @patch("requests.get")
    def test_get_weather_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "main": {"temp": 20},
            "weather": [{"description": "sunny"}]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = self.tool.get_weather("London")
        self.assertEqual(result["city"], "London")
        self.assertEqual(result["temp"], 20)
        self.assertEqual(result["condition"], "sunny")

    @patch("requests.get")
    def test_get_weather_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("API Error")
        result = self.tool.get_weather("InvalidCity")
        self.assertIn("error", result)

class TestAirQualityTool(unittest.TestCase):
    def setUp(self):
        self.tool = AirQualityTool()
        os.environ["OPENWEATHER_API_KEY"] = "test_key"

    @patch("requests.get")
    def test_get_air_quality_success(self, mock_get):
        # Mocking two calls: one for geo, one for aqi
        mock_geo_response = MagicMock()
        mock_geo_response.json.return_value = [{"lat": 10, "lon": 20}]
        mock_geo_response.status_code = 200

        mock_aqi_response = MagicMock()
        mock_aqi_response.json.return_value = {"list": [{"main": {"aqi": 1}}]}
        mock_aqi_response.status_code = 200

        mock_get.side_effect = [mock_geo_response, mock_aqi_response]

        result = self.tool.get_air_quality("Paris")
        self.assertEqual(result["city"], "Paris")
        self.assertEqual(result["aqi"], 1)
        self.assertEqual(result["level"], "Good")

    @patch("requests.get")
    def test_get_air_quality_failure(self, mock_get):
         mock_get.side_effect = requests.exceptions.RequestException("API Error")
         result = self.tool.get_air_quality("InvalidCity")
         self.assertIn("error", result)

if __name__ == "__main__":
    unittest.main()
