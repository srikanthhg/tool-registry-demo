from tools.weather_tool import get_weather


def test_weather():
    data = get_weather("Singapore")

    assert "current_condition" in data
# def test_weather():
#     data = get_weather("Singapore")

#     assert isinstance(data, str)
#     assert "weather" in data.lower()