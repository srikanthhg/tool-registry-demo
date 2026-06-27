from tools.rest_api_tool import get_post


def test_rest():
    data = get_post(1)

    assert data["id"] == 1