from datetime import datetime
import pytz

def get_current_datetime(timezone: str) -> str:
    """
    Retrieves the current date and time in the specified timezone.
    
    Args:
        timezone (str): The timezone name (e.g., 'UTC', 'America/New_York', 
                        'Asia/Tokyo', 'Europe/London').
        
    Returns:
        str: Current date and time in ISO 8601 format with timezone info.
    """
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)
        return current_time.isoformat()
    except pytz.exceptions.UnknownTimeZoneError:
        return f"Error: Unknown timezone '{timezone}'. Use IANA timezone names like 'UTC', 'America/New_York', 'Asia/Tokyo'."