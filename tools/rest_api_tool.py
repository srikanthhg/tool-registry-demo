import requests
import json

def get_post(post_id: int) -> str:
    """
    Retrieves a specific blog post by its unique ID from the JSONPlaceholder API.

    Args:
        post_id (int): The unique numerical identifier of the post to retrieve.

    Returns:
        str: A JSON-formatted string containing the post's userId, id, title, and body.
    """
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    
    # Convert dict to JSON string
    return json.dumps(response.json())