from pymavlink import mavutil

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

    def disarm(self):
        self.connection.mav.command_long_send(
            self.connection.target_system,
            self.connection.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0, 0, 0, 0, 0, 0, 0, 0
        )
        print("Sent disarm command")
        
    def takeoff(self, altitude=10):
        self.connection.mav.command_long_send(
            self.connection.target_system,
            self.connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0,
            0, 0, 0, 0, 0, 0, altitude
        )
        return {"status": f"Taking off to {altitude} meters"}
    
    def change_mode(self, mode_id: int):
        self.connection.set_mode(mode_id)

    def get_modes(self):
        return self.connection.mode_mapping()