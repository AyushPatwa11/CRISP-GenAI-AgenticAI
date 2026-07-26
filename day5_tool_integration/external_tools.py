import requests
from typing import Dict, Any

def get_live_weather(city: str) -> str:
    """Fetches real-time weather using Open-Meteo REST API (Free, no API key required)."""
    try:
        # Step 1: Geocoding lookup for lat/lon
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        geo_res = requests.get(geo_url, timeout=3).json()
        
        if not geo_res.get("results"):
            return f"Weather Error: Could not find location coordinates for '{city}'."
        
        loc = geo_res["results"][0]
        lat, lon = loc["latitude"], loc["longitude"]
        city_name = loc.get("name", city)
        country = loc.get("country", "")
        
        # Step 2: Fetch weather forecast data
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        w_res = requests.get(weather_url, timeout=3).json()
        
        curr = w_res.get("current_weather", {})
        temp = curr.get("temperature", "N/A")
        windspeed = curr.get("windspeed", "N/A")
        
        return f"Weather in {city_name}, {country}: {temp}°C, Wind Speed: {windspeed} km/h."
    except Exception as e:
        return f"Weather Service Error: {str(e)}"

def search_web_duckduckgo(query: str) -> str:
    """Performs web search using DDGS with fast 3-second timeout."""
    try:
        try:
            from ddgs import DDGS
        except ImportError:
            from duckduckgo_search import DDGS

        ddgs = DDGS(timeout=4)
        results = list(ddgs.text(query, max_results=3))
        
        if not results:
            # Clean search query fallback
            cleaned = query.replace("will release", "").replace("release date", "").strip()
            results = list(ddgs.text(cleaned, max_results=3))

        if not results:
            return f"No web search results found for '{query}'."
        
        snippets = [f"📌 [{r.get('title', 'Result')}]({r.get('href', '#')})\n{r.get('body', '')}" for r in results]
        return "\n\n".join(snippets)
    except Exception as e:
        return f"Web Search Error: {str(e)}"

def create_calendar_invite_mock(title: str, date_str: str, attendees: str) -> str:
    """Generates structured calendar meeting invite parameters."""
    return f"📅 Calendar Invite Created: '{title}' on {date_str} with {attendees}. Notification sent!"
