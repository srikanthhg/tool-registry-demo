import requests


def get_weather(city: str):
    """
    Returns weather information from wttr.in
    """

    url = f"https://wttr.in/{city}?format=j1"

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    return response.json()


"""
This is a normal Python function.

Later it becomes a Databricks Tool.
"""