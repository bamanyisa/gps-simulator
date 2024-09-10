import time
import logging
from typing import List, Tuple
from .osrm_service import get_route
from .traccar_service import send_coordinates_to_traccar
from .route_utils import interpolate_route
from .exceptions import OSRMRequestError

class GPSSimulator:

    def __init__(self, server_url: str, device_id: str, waypoints: List[Tuple[float, float]], frequency: int = 2):
        self.server_url = server_url
        self.device_id = device_id
        self.waypoints = waypoints
        self.frequency = frequency

    def run(self) -> None:
        print("Starting GPSSimulator...")
        print(f"Device ID: {self.device_id}")
        print(f"Waypoints: {self.waypoints}")


        try:
            print("Fetching route from OSRM...")
            route = get_route(self.waypoints)['routes'][0]
            
            coordinates = route['geometry']['coordinates']
            duration = route['duration']
            distance = route['distance']
            
            print(f"Route fetched successfully. Duration: {duration} seconds, Distance: {distance} meters")
            
        except OSRMRequestError as e:
            logging.error(f"OSRM request error: {e}")
            return
        except KeyError as e:
            logging.error(f"Missing expected field in OSRM response: {e}")
            return

        print("Interpolating route...")
        interpolated_route = interpolate_route(coordinates, distance, duration, self.frequency)
        
        

        print("Starting simulation...")
        self.simulate(interpolated_route)
        print("Simulation complete.")
        
    def simulate(self, interpolated_route: List[dict]) -> None:
        for point in interpolated_route:
            params = {
                'server_url': self.server_url,
                'id': self.device_id,
                'valid': 'true',
                'timestamp': int(time.time()),
                'lat': point['lat'],
                'lon': point['lon'],
                'location': None,
                'cell': None,
                'wifi': None,
                'speed': point['speed'],
                'altitude': None,
                'accuracy': None,
                'hdop': None,
                'batt': 100,
                'driverUniqueId': None,
                'charge': 'true',
            }
            print(f"Sending coordinates to Traccar: Lat={point['lat']}, Lon={point['lon']}, Device ID={self.device_id}")
            send_coordinates_to_traccar(params)
            time.sleep(self.frequency)

