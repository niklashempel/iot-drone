import requests
from pymavlink import mavutil
from drone import Drone

class MAVLink2Rest():
    def __init__(self, wsapi='http://0.0.0.0:8088'):
        self.wsapi = wsapi
        self.drone = Drone()
        self.drone.connect()

    def get_heartbeat(self):
        r = requests.get('http://0.0.0.0:8088/v1/mavlink/vehicles/1/components/1/messages/HEARTBEAT')
        return r.json()
    
    def is_armed(self):
        heartbeat = self.get_heartbeat()
        return heartbeat['message']['base_mode']['bits'] & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED != 0
    
    def get_current_mode(self):
        heartbeat = self.get_heartbeat()
        custom_mode = heartbeat['message']['custom_mode']
        print(f"Current mode ID: {custom_mode}")
        modes = self.drone.get_modes()
        for mode_name, mode_id in modes.items():
            if mode_id == custom_mode:
                return mode_name
        return "Unknown"
    