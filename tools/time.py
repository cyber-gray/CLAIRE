# tools/time_tool.py

from langchain.tools import tool
from datetime import datetime
import pytz

@tool
def get_time(city: str = "local") -> str:
    """Returns the current date and time. If city is provided, returns date and time for that city, otherwise returns local date and time."""
    try:
        if city.lower() == "local":
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%A, %B %d, %Y at %I:%M %p")
            return f"Today is {formatted_datetime}."
        
        city_timezones = {
            "new york": "America/New_York",
            "london": "Europe/London", 
            "tokyo": "Asia/Tokyo",
            "sydney": "Australia/Sydney",
            "los angeles": "America/Los_Angeles",
            "chicago": "America/Chicago",
            "paris": "Europe/Paris",
            "berlin": "Europe/Berlin",
            "toronto": "America/Toronto",
        }
        city_key = city.lower()
        if city_key not in city_timezones:
            return f"Sorry, I don't know the timezone for {city}. Available cities: {', '.join(city_timezones.keys())}"

        timezone = pytz.timezone(city_timezones[city_key])
        current_datetime = datetime.now(timezone)
        formatted_datetime = current_datetime.strftime("%A, %B %d, %Y at %I:%M %p")
        return f"In {city.title()}, it's {formatted_datetime}."
    except Exception as e:
        return f"Error: {e}"
