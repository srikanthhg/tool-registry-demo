from tools.datetime_tool import get_current_datetime

def test_datetime_utc():
    result = get_current_datetime("UTC")
    
    assert isinstance(result, str)
    assert len(result) > 0
    assert "+" in result or "Z" in result or "UTC" in result

def test_datetime_invalid_timezone():
    result = get_current_datetime("Invalid/Timezone")
    
    assert "Error" in result
    assert "Unknown timezone" in result