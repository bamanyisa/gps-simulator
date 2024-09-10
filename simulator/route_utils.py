from geopy.distance import geodesic
from typing import List, Tuple

def interpolate_route(coordinates: List[Tuple[float, float]], distance: float, duration: float, frequency: int) -> List[dict]:
    interpolated_route = []
    num_points = len(coordinates)
    average_speed = distance / duration
    interval_duration = frequency

    for i in range(num_points - 1):
        start_point = coordinates[i]
        end_point = coordinates[i + 1]
        segment_distance = geodesic(start_point[::-1], end_point[::-1]).meters
        segment_time = segment_distance / average_speed
        num_intervals = int(segment_time / interval_duration)

        for j in range(num_intervals):
            lat = start_point[1] + j * (end_point[1] - start_point[1]) / num_intervals
            lon = start_point[0] + j * (end_point[0] - start_point[0]) / num_intervals
            
            interpolated_route.append({
                'lat': lat,
                'lon': lon,
                'speed': average_speed * 1.94384
            })

    interpolated_route.append({
        'lat': coordinates[-1][1],
        'lon': coordinates[-1][0],
        'speed': average_speed * 1.94384
    })
    
    return interpolated_route
