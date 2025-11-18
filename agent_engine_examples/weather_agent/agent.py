import requests
from google.adk.agents import Agent


def get_lat_lon(city: str):
    """
    Gets the latitude and longitude for a given city name.
    
    Args:
        city: The name of the city (e.g., "Anchorage").
        
    Returns:
        A tuple of (latitude, longitude) or (None, None) if not found.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city,
        "format": "json",
        "limit": 1
    }

    try:
        response = requests.get(url, params=params, headers={"User-Agent": "city-locator/1.0"})
        response.raise_for_status() # Raises an exception for bad status codes
        data = response.json()

        if not data:
            return None, None  

        lat = data[0]["lat"]
        lon = data[0]["lon"]
        return lat, lon
    except requests.RequestException as e:
        print(f"Error getting lat/lon: {e}")
        return None, None

def get_temperature_f(lat: float, lon: float):
    """
    Gets the current temperature in Fahrenheit for a given latitude and longitude.
    
    Args:
        lat: The latitude.
        lon: The longitude.
        
    Returns:
        The current temperature in Fahrenheit, or None if an error occurs.
    """
    if lat is None or lon is None:
        return None

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m",
        "temperature_unit": "fahrenheit"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data["current"]["temperature_2m"]
    except requests.RequestException as e:
        print(f"Error getting temperature: {e}")
        return None
    except KeyError:
        print("Error parsing temperature data")
        return None


root_agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash",
    description="A bot that can get the weather and suggest clothing.",
    instruction="You are a helpful assistant. Use your tools to answer questions about the weather and what to wear. "
                "If you need to find the weather, you must first get the latitude and longitude, "
                "then get the temperature, and then suggest the clothing.",
    tools=[
        get_lat_lon,
        get_temperature_f
    ],
)
