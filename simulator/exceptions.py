class ConfigNotFoundError(Exception):
    """Exception raised for errors related to the configuration file not being found."""
    pass

class InvalidWaypointsError(Exception):
    """Exception raised for invalid waypoints."""
    pass

class OSRMRequestError(Exception):
    """Exception raised for errors related to OSRM requests."""
    pass

class TraccarError(Exception):
    """Exception raised for errors related to Traccar server requests."""
    def __init__(self, device_id: str, message: str):
        super().__init__(f"Failed to send data to Traccar for device {device_id}: {message}")
