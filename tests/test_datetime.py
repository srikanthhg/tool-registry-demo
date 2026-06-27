from tools.datetime_tool import get_current_datetime

def test_datetime_utc():
    result = get_current_datetime("UTC")
    
    # Should return a string with current datetime
    assert isinstance(result, str)
    assert len(result) > 0
    # Should contain timezone info
    assert "+" in result or "Z" in result or result.endswith("UTC")

def test_datetime_invalid_timezone():
    result = get_current_datetime("Invalid/Timezone")
    
    # Should return an error message
    assert "Error" in result
    assert "Unknown timezone" in result