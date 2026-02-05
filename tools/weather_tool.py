import requests
import os

class WeatherTool:
    """
    A tool for fetching current weather data for a given city using OpenWeatherMap API.
    """
    def get_weather(self, city: str):
        """
        Fetches the current weather for a specified city.

        Args:
            city (str): The name of the city.

        Returns:
            dict: A dictionary containing the city name, temperature, and weather condition.
                  Returns an error dictionary if the API call fails.
        """
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            return {"error": "Missing OPENWEATHER_API_KEY environment variable"}

        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={api_key}&units=metric"
        )
        
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status() # Raise HTTPError for bad responses (4xx, 5xx)
            data = r.json()

            return {
                "city": city,
                "temp": data["main"]["temp"],
                "condition": data["weather"][0]["description"]
            }
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch weather data: {str(e)}"}
        except (KeyError, IndexError) as e:
             return {"error": f"Failed to parse weather data: {str(e)}"}
