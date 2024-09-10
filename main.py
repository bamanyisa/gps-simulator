import threading
import logging
from simulator.config import Config
from simulator.simulator import GPSSimulator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main() -> None:
    try:
        config = Config('config/config.json')
    except Exception as e:
        logging.error(e)
        return

    server_url = config.server_url
    devices = config.devices
    frequency = config.frequency
    
    threads = []
    for device in devices:
        device_name = device['serial_number']
        waypoints = device['waypoints']
        
        if len(waypoints) >= 2:
            waypoints = [(point[0], point[1]) for point in waypoints] 
            tracker = GPSSimulator(server_url, device_name, waypoints, frequency)
            
            thread = threading.Thread(target=tracker.run)
            thread.start()
            threads.append(thread)
        else:
            logging.error(f"Not enough waypoints for device {device_name}")

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
