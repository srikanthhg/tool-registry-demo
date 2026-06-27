
# import requests
# import json
# def get_weather(city: str) -> str:
#     """
#     Returns weather information from wttr.in
#     """


#     url = f"https://wttr.in/{city}?format=j1"

#     response = requests.get(url, timeout=20)
#     response.raise_for_status()

#     return json.dumps(response.json())

# print(get_weather("Hyderabad"))

import json
import urllib.request

def get_weather(city: str) -> str:
    """
    Get current weather information for a city.

    Fetches live weather data from wttr.in and returns
    a human-readable summary including temperature and condition.
    """

    url = f"https://wttr.in/{city}?format=j1"

    with urllib.request.urlopen(url, timeout=20) as response:
        data = json.loads(response.read().decode("utf-8"))

    current = data["current_condition"][0]

    temp_c = current["temp_C"]
    desc = current["weatherDesc"][0]["value"]
    humidity = current["humidity"]
    feels_like = current["FeelsLikeC"]

    return (
        f"The weather in {city} is {desc}. "
        f"Temperature is {temp_c}°C, feels like {feels_like}°C, "
        f"humidity is {humidity}%."
    )


"""
This is a normal Python function.

Later it becomes a Databricks Tool.
"""