from pymavlink import mavutil
import time

class Drone:
    def __init__(self):
        self.connection = None

    def connect(self, address='udp:127.0.0.1:14550'):
        # Connect to MAVProxy's UDP interface
        self.connection = mavutil.mavlink_connection(address)
        print("Waiting for heartbeat...")
        self.connection.wait_heartbeat()
        print("Heartbeat from system (system %u component %u)" % (self.connection.target_system, self.connection.target_component))
        
    
    def arm(self):
        self.connection.mav.command_long_send(
            self.connection.target_system,
            self.connection.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0, 1, 0, 0, 0, 0, 0, 0
        )
        print("Sent arm command")
        for _ in range(3):
            response = self.connection.recv_match(type='HEARTBEAT', blocking=False, timeout=3)
            if response:
                armed = response.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
                if armed:
                    print(f"Vehicle armed")
                    return {"status": "Vehicle armed"}
            time.sleep(0.5)
        print(f"Vehicle not armed")
        return {"status": "Vehicle not armed"}

    def disarm(self):
        self.connection.mav.command_long_send(
            self.connection.target_system,
            self.connection.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0, 0, 0, 0, 0, 0, 0, 0
        )
        print("Sent disarm command")
        for _ in range(3):
            response = self.connection.recv_match(type='HEARTBEAT', blocking=False, timeout=3)
            if response:
                armed = response.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
                if not armed:
                    print(f"Vehicle disarmed")
                    return {"status": "Vehicle disarmed"}
            time.sleep(0.5)
            
    def takeoff(self, altitude=10):
        self.connection.mav.command_long_send(
            self.connection.target_system,
            self.connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0,
            0, 0, 0, 0, 0, 0, altitude
        )
        return {"status": f"Taking off to {altitude} meters"}
    
    def land(self):
        self.connection.mav.command_long_send(
            self.connection.target_system,
            self.connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_LAND,
            0,
            0, 0, 0, 0, 0, 0, 0
        )
        return {"status": "Landing"}