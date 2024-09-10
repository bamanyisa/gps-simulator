import requests
from typing import List, Tuple, Dict, Any
from .exceptions import OSRMRequestError

def get_route(coordinates: List[Tuple[float, float]]) -> Dict[str, Any]:
    
    try:
        coordinates_str = ";".join([f"{coord[0]},{coord[1]}" for coord in coordinates])
        url = (f"http://router.project-osrm.org/route/v1/driving/{coordinates_str}?"
               "overview=full&"
               "geometries=geojson&"
               "annotations=true&"
               "steps=true")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        response_json = response.json()        
        
        return response_json
    except requests.exceptions.RequestException as req_err:
        raise OSRMRequestError(f"An error occurred while requesting the route: {req_err}")
