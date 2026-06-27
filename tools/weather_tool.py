
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
    url = f"https://wttr.in/{city}?format=j1"

    with urllib.request.urlopen(url, timeout=20) as response:
        data = response.read()

    return json.dumps(json.loads(data))


"""
This is a normal Python function.

Later it becomes a Databricks Tool.
"""