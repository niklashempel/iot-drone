from pymavlink import mavutil

# Connect to MAVProxy's UDP interface
master = mavutil.mavlink_connection('udp:127.0.0.1:14550')

# Wait for a heartbeat from the MAVLink system
master.wait_heartbeat()

# Send a command (e.g., ARM the vehicle)
master.mav.command_long_send(
    master.target_system,    # Target system
    master.target_component, # Target component
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,  # Command
    0,  # Confirmation
    1,  # Param1 (1 to arm, 0 to disarm)
    0, 0, 0, 0, 0, 0  # Unused parameters
)
