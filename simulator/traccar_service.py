import requests
from .exceptions import TraccarError

def send_coordinates_to_traccar(params: dict) -> None:
    
    server_url = params.pop('server_url')

    try:
        response = requests.get(server_url, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        raise TraccarError(params.get('id', 'unknown'), str(e))
