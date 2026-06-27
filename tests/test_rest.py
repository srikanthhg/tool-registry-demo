import json
from tools.rest_api_tool import get_post

def test_rest():
    data_str = get_post(1)
    data = json.loads(data_str)  # Parse the JSON string back to dict
    
    assert data["id"] == 1