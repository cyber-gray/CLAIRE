"""
Weather API Tool for CLAIRE
Provides current weather and forecasts
"""

from langchain.tools import tool
import requests
import os
from typing import Optional
import logging

@tool
def get_current_weather(location: str) -> str:
    """
    Get current weather conditions for a specified location.
    
    Args:
        location: City name, zip code, or "lat,lon" coordinates
    
    Returns:
        Current weather information including temperature, conditions, and forecast
    """
    try:
        api_key = os.getenv("WEATHER_API_KEY")
        if not api_key:
            return "❌ Weather API key not configured. Please set WEATHER_API_KEY environment variable."
        
        # OpenWeatherMap current weather endpoint
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric"  # Celsius
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract weather data
        city = data.get("name", location)
        country = data.get("sys", {}).get("country", "")
        temp = data.get("main", {}).get("temp", "N/A")
        feels_like = data.get("main", {}).get("feels_like", "N/A")
        humidity = data.get("main", {}).get("humidity", "N/A")
        pressure = data.get("main", {}).get("pressure", "N/A")
        
        weather = data.get("weather", [{}])[0]
        description = weather.get("description", "").title()
        main_weather = weather.get("main", "")
        
        wind = data.get("wind", {})
        wind_speed = wind.get("speed", "N/A")
        wind_deg = wind.get("deg", "N/A")
        
        visibility = data.get("visibility", "N/A")
        if visibility != "N/A":
            visibility = f"{visibility / 1000:.1f} km"
        
        # Format result
        result = f"## 🌤️ Current Weather for {city}"
        if country:
            result += f", {country}"
        result += "\n\n"
        
        result += f"**Conditions:** {description} ({main_weather})\n"
        result += f"**Temperature:** {temp}°C (feels like {feels_like}°C)\n"
        result += f"**Humidity:** {humidity}%\n"
        result += f"**Pressure:** {pressure} hPa\n"
        
        if wind_speed != "N/A":
            result += f"**Wind:** {wind_speed} m/s"
            if wind_deg != "N/A":
                result += f" at {wind_deg}°"
            result += "\n"
        
        if visibility != "N/A":
            result += f"**Visibility:** {visibility}\n"
        
        # Convert to Fahrenheit for US users
        if temp != "N/A":
            temp_f = (float(temp) * 9/5) + 32
            feels_like_f = (float(feels_like) * 9/5) + 32
            result += f"\n**US Units:** {temp_f:.1f}°F (feels like {feels_like_f:.1f}°F)"
        
        return result
        
    except requests.RequestException as e:
        logging.error(f"Error fetching weather: {e}")
        return f"Error fetching weather data: {str(e)}"
    except Exception as e:
        logging.error(f"Error in get_current_weather: {e}")
        return f"Error getting weather: {str(e)}"

@tool
def get_weather_forecast(location: str, days: int = 3) -> str:
    """
    Get weather forecast for a specified location.
    
    Args:
        location: City name, zip code, or "lat,lon" coordinates
        days: Number of days to forecast (1-5, default: 3)
    
    Returns:
        Weather forecast information
    """
    try:
        api_key = os.getenv("WEATHER_API_KEY")
        if not api_key:
            return "❌ Weather API key not configured. Please set WEATHER_API_KEY environment variable."
        
        # Limit days to 5 (free tier limit)
        days = min(max(days, 1), 5)
        
        # OpenWeatherMap 5-day forecast endpoint
        url = "http://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric",
            "cnt": days * 8  # 8 forecasts per day (every 3 hours)
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        city = data.get("city", {}).get("name", location)
        country = data.get("city", {}).get("country", "")
        forecasts = data.get("list", [])
        
        if not forecasts:
            return f"No forecast data available for {location}"
        
        # Format result
        result = f"## 📅 {days}-Day Weather Forecast for {city}"
        if country:
            result += f", {country}"
        result += "\n\n"
        
        # Group forecasts by day
        daily_forecasts = {}
        for forecast in forecasts:
            dt_txt = forecast.get("dt_txt", "")
            if dt_txt:
                date = dt_txt.split(" ")[0]
                if date not in daily_forecasts:
                    daily_forecasts[date] = []
                daily_forecasts[date].append(forecast)
        
        # Display daily summaries
        for i, (date, day_forecasts) in enumerate(list(daily_forecasts.items())[:days]):
            if not day_forecasts:
                continue
                
            # Get midday forecast (closest to 12:00)
            midday_forecast = min(day_forecasts, 
                                key=lambda x: abs(12 - int(x.get("dt_txt", "").split(" ")[1].split(":")[0])))
            
            temp = midday_forecast.get("main", {}).get("temp", "N/A")
            temp_min = min([f.get("main", {}).get("temp_min", float('inf')) for f in day_forecasts])
            temp_max = max([f.get("main", {}).get("temp_max", float('-inf')) for f in day_forecasts])
            
            weather = midday_forecast.get("weather", [{}])[0]
            description = weather.get("description", "").title()
            
            humidity = midday_forecast.get("main", {}).get("humidity", "N/A")
            
            result += f"### Day {i+1}: {date}\n"
            result += f"**Conditions:** {description}\n"
            result += f"**Temperature:** {temp_min:.1f}°C - {temp_max:.1f}°C\n"
            result += f"**Humidity:** {humidity}%\n\n"
        
        return result
        
    except requests.RequestException as e:
        logging.error(f"Error fetching forecast: {e}")
        return f"Error fetching weather forecast: {str(e)}"
    except Exception as e:
        logging.error(f"Error in get_weather_forecast: {e}")
        return f"Error getting weather forecast: {str(e)}"
