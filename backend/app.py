import time
from flask import Flask, request, jsonify, render_template
from drone import Drone
from api import MAVLink2Rest

app = Flask(__name__)
api = MAVLink2Rest()

drone = Drone()
drone.connect()

# Serve the HTML file
@app.route('/')
@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def send_command():
    command = request.json.get("command")
    if not command:
        return jsonify({"error": "No command provided"}), 400

    if command == "arm":
        drone.arm()
        time.sleep(1)
        armed = api.is_armed()
        return jsonify(armed), 200
    elif command == "disarm":
        drone.disarm()
        time.sleep(1)
        disarmed = not api.is_armed()
        return jsonify(disarmed), 200
    elif command == "takeoff":
        return jsonify(drone.takeoff()), 200
    elif command == "land":
        return jsonify(drone.land()), 200
    elif command == "change_mode":
        mode = request.json.get("mode")
        drone.change_mode(mode)
        current_mode = api.get_current_mode()
        return jsonify({"current_mode": current_mode}), 200
    else:
        return jsonify({"error": "Unsupported command"}), 400

@app.route('/status', methods=['GET'])
def get_status():
    current_mode = api.get_current_mode()
    print(current_mode)
    return jsonify(current_mode), 200

@app.route('/modes', methods=['GET'])
def get_modes():
    modes = drone.get_modes()
    return jsonify(list(modes.keys())), 200

@app.route('/modes/current', methods=['GET'])
def get_current_mode():
    current_mode = api.get_current_mode()
    return jsonify(current_mode), 200
                        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)