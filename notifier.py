from plyer import notification
import time

def send_notification(title, message, timeout=10):
    """
    Send a desktop notification.
    
    Args:
    - title (str): The title of the notification.
    - message (str): The body of the notification.
    - timeout (int): Duration in seconds (default is 10 seconds).
    """
    try:
        notification.notify(
            title=title,
            message=message,
            timeout=timeout,  # seconds
            app_name="NeoMind Assistant"
        )
        print(f"[NeoMind Notification] Sent: {title} - {message}")
    except Exception as e:
        print(f"Failed to send notification: {e}")
