import requests


def get_post(post_id: int) -> dict:
    """
    Returns a sample REST API response.
    """

    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    return response.json()