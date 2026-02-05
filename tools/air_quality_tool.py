import requests
import os

class AirQualityTool:
    """
    A tool for fetching air quality data for a given city using OpenWeatherMap API.
    """
    def get_air_quality(self, city: str):
        """
        Fetches the air quality index (AQI) for a specified city.

        Args:
            city (str): The name of the city.

        Returns:
            dict: A dictionary containing the city name, AQI, and qualitative level.
                  Returns an error dictionary if the API call fails.
        """
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
             return {"error": "Missing OPENWEATHER_API_KEY environment variable"}

        try:
            # Step 1: Get lat/lon from city
            geo_url = (
                f"http://api.openweathermap.org/geo/1.0/direct"
                f"?q={city}&limit=1&appid={api_key}"
            )
            geo_res = requests.get(geo_url, timeout=10)
            geo_res.raise_for_status()
            geo_data = geo_res.json()
            
            if not geo_data:
                return {"error": f"Could not find coordinates for city: {city}"}

            lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]

            # Step 2: Get AQI
            aqi_url = (
                f"http://api.openweathermap.org/data/2.5/air_pollution"
                f"?lat={lat}&lon={lon}&appid={api_key}"
            )
            data = requests.get(aqi_url, timeout=10).json()

            aqi = data["list"][0]["main"]["aqi"]

            return {
                "city": city,
                "aqi": aqi,
                "level": self.aqi_level(aqi)
            }
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch air quality data: {str(e)}"}
        except (KeyError, IndexError) as e:
            return {"error": f"Failed to parse air quality data: {str(e)}"}


    def aqi_level(self, aqi):
        """
        Maps the AQI value to a qualitative description.
        """
        levels = {
            1: "Good",
            2: "Fair",
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }
        return levels.get(aqi, "Unknown")
