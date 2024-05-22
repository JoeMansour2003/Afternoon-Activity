import requests
from dotenv import load_dotenv
import os

load_dotenv()

def weather_data(request):
    lat = os.getenv("lat")
    lon = os.getenv("lon")
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")

    try:
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}')
        response.raise_for_status()  # Raises a HTTPError if the response status is 4xx, 5xx
    except requests.exceptions.RequestException as e:
        # Log the error and return default weather data
        print(f"Error fetching weather data: {e}")
        return {
            'weather_description': 'N/A',
            'weather': 'N/A',
            'weather_icon': 'N/A',
            'chance_of_rain': 'N/A',
        }
    weather_data = response.json()

    weather_description = weather_data['weather'][0]['description']
    chance_of_rain = weather_data['rain']['3h'] if 'rain' in weather_data and '3h' in weather_data['rain'] else 0
    weather_in_kelvin = weather_data['main']['feels_like']
    weather_in_celsius = weather_in_kelvin - 273.15
    weather_icon = weather_data['weather'][0]['icon']

    

    return {
        'weather_description': weather_description,
        'weather': round(weather_in_celsius,1),
        'weather_icon': weather_icon,
        'chance_of_rain': chance_of_rain,
    }