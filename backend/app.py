from flask import Flask, request, jsonify, render_template
from pymavlink import mavutil

app = Flask(__name__)

# Connect to MAVProxy's UDP interface
master = mavutil.mavlink_connection('udp:127.0.0.1:14550')
master.wait_heartbeat()

# Serve the HTML file
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def send_command():
    command = request.json.get("command")
    if not command:
        return jsonify({"error": "No command provided"}), 400

    if command == "arm":
        master.mav.command_long_send(
            master.target_system,
            master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0, 1, 0, 0, 0, 0, 0, 0
        )
        return jsonify({"status": "Vehicle armed"})
    elif command == "disarm":
        master.mav.command_long_send(
            master.target_system,
            master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0, 0, 0, 0, 0, 0, 0, 0
        )
        return jsonify({"status": "Vehicle disarmed"})
    else:
        return jsonify({"error": "Unsupported command"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)