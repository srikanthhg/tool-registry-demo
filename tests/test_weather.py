from tools.weather_tool import get_weather


def test_weather():
    data = get_weather("Singapore")

    assert "current_condition" in data