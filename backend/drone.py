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
    
    def land(self):
        self.connection.mav.command_long_send(
            self.connection.target_system,
            self.connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_LAND,
            0,
            0, 0, 0, 0, 0, 0, 0
        )
        return {"status": "Landing"}
    
    def change_mode(self, mode: str):
        if mode not in self.connection.mode_mapping():
            return {"error": f"Mode {mode} not supported. Try: {list(self.connection.mode_mapping().keys())}"}
        mode_id = self.connection.mode_mapping()[mode]
        # Set new mode
        self.connection.set_mode(mode_id)
        for _ in range(0, 10):
            # Wait for ACK command
            # Would be good to add mechanism to avoid endlessly blocking
            # if the autopilot sends a NACK or never receives the message
            ack_msg = self.connection.recv_match(type='COMMAND_ACK', blocking=True)
            ack_msg = ack_msg.to_dict()

            # Continue waiting if the acknowledged command is not `set_mode`
            if ack_msg['command'] != mavutil.mavlink.MAV_CMD_DO_SET_MODE:
                continue

            # Print the ACK result !
            print(mavutil.mavlink.enums['MAV_RESULT'][ack_msg['result']].description)
            break

    def get_modes(self):
        return self.connection.mode_mapping()