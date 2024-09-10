import json
from typing import Dict, Any, List
from .exceptions import ConfigNotFoundError, InvalidWaypointsError, OSRMRequestError, TraccarError

class Config:
    def __init__(self, config_file: str):
        self.config_file = config_file
        
        try:
            self.config = self.load_config()
        except FileNotFoundError:
            raise ConfigNotFoundError(f"Configuration file '{self.config_file}' not found.")
        
        self.server_url = self.get_server_url()
        self.frequency = self.get_frequency()
        self.devices = self.get_all_devices()

    def load_config(self) -> Dict[str, Any]:
        with open(self.config_file, 'r') as file:
            return json.load(file)

    def get_server_url(self) -> str:
        return self.config.get('Server', {}).get('url', None)

    def get_frequency(self) -> int:
        return self.config.get('Server', {}).get('frequency', None)

    def get_all_devices(self) -> List[Dict[str, Any]]:
        devices = self.config.get('devices', [])
        for device in devices:
            if not self.validate_waypoints(device.get('waypoints', [])):
                raise InvalidWaypointsError(f"Invalid waypoints for device {device.get('name', 'Unknown')}")
        return devices

    @staticmethod
    def validate_waypoints(waypoints: List[List[float]]) -> bool:
        if len(waypoints) < 2:
            return False
        for waypoint in waypoints:
            if not isinstance(waypoint, list) or len(waypoint) != 2:
                return False
            lat, lon = waypoint
            if not (isinstance(lat, (int, float)) and isinstance(lon, (int, float))):
                return False
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                return False
        return True
