# tools/time_tool.py

from langchain.tools import tool
from datetime import datetime, timedelta
import pytz
import calendar

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
            "singapore": "Asia/Singapore",
            "mumbai": "Asia/Kolkata",
            "dubai": "Asia/Dubai",
            "moscow": "Europe/Moscow",
            "beijing": "Asia/Shanghai",
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

@tool
def get_date_info(date_query: str = "today") -> str:
    """
    Get detailed date information including day of week, week number, days until weekend, etc.
    
    Args:
        date_query: "today", "tomorrow", "yesterday", or specific date like "2025-07-30"
    
    Returns:
        Detailed date information
    """
    try:
        now = datetime.now()
        
        if date_query.lower() == "today":
            target_date = now
        elif date_query.lower() == "tomorrow":
            target_date = now + timedelta(days=1)
        elif date_query.lower() == "yesterday":
            target_date = now - timedelta(days=1)
        else:
            # Try to parse specific date
            try:
                target_date = datetime.strptime(date_query, "%Y-%m-%d")
            except ValueError:
                return f"Invalid date format. Use 'today', 'tomorrow', 'yesterday', or YYYY-MM-DD format."
        
        # Calculate various date info
        day_name = target_date.strftime("%A")
        month_name = target_date.strftime("%B")
        day_of_year = target_date.timetuple().tm_yday
        week_number = target_date.isocalendar()[1]
        
        # Days until weekend
        days_until_weekend = (5 - target_date.weekday()) % 7
        if days_until_weekend == 0 and target_date.weekday() >= 5:
            days_until_weekend = 0  # Already weekend
        
        # Quarter information
        quarter = (target_date.month - 1) // 3 + 1
        
        # Days in month
        days_in_month = calendar.monthrange(target_date.year, target_date.month)[1]
        
        result = f"## 📅 Date Information for {target_date.strftime('%B %d, %Y')}\n\n"
        result += f"**Day:** {day_name}\n"
        result += f"**Week:** Week {week_number} of {target_date.year}\n"
        result += f"**Day of Year:** Day {day_of_year} of 365\n"
        result += f"**Quarter:** Q{quarter} {target_date.year}\n"
        result += f"**Days in {month_name}:** {days_in_month}\n"
        
        if days_until_weekend == 0 and target_date.weekday() >= 5:
            result += f"**Weekend Status:** It's the weekend! 🎉\n"
        elif days_until_weekend == 0:
            result += f"**Weekend Status:** Weekend starts today! 🎉\n"
        else:
            result += f"**Days Until Weekend:** {days_until_weekend} days\n"
        
        # Season (Northern Hemisphere)
        month = target_date.month
        if month in [12, 1, 2]:
            season = "Winter ❄️"
        elif month in [3, 4, 5]:
            season = "Spring 🌸"
        elif month in [6, 7, 8]:
            season = "Summer ☀️"
        else:
            season = "Autumn 🍂"
        
        result += f"**Season:** {season}\n"
        
        return result
        
    except Exception as e:
        return f"Error getting date information: {str(e)}"

@tool
def get_world_clocks() -> str:
    """
    Get current time in major world cities.
    
    Returns:
        Current time in multiple timezones
    """
    try:
        major_cities = {
            "New York": "America/New_York",
            "London": "Europe/London",
            "Paris": "Europe/Paris",
            "Tokyo": "Asia/Tokyo",
            "Sydney": "Australia/Sydney",
            "Dubai": "Asia/Dubai",
            "Singapore": "Asia/Singapore",
            "Los Angeles": "America/Los_Angeles"
        }
        
        result = "## 🌍 World Clocks\n\n"
        
        for city, timezone_str in major_cities.items():
            try:
                timezone = pytz.timezone(timezone_str)
                city_time = datetime.now(timezone)
                formatted_time = city_time.strftime("%I:%M %p")
                formatted_date = city_time.strftime("%a, %b %d")
                
                result += f"**{city}:** {formatted_time} ({formatted_date})\n"
            except Exception:
                result += f"**{city}:** Time unavailable\n"
        
        return result
        
    except Exception as e:
        return f"Error getting world clocks: {str(e)}"
