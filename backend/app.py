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
    return jsonify(modes), 200

@app.route('/mode/<int:mode_id>', methods=['GET'])
def get_mode(mode_id):
    modes = drone.get_modes()
    # Invert the dictionary
    modes = {v: k for k, v in modes.items()}
    print(modes)
    mode_name = modes[mode_id]
    return jsonify({"mode_name": mode_name, "mode_id": mode_id}), 200

@app.route('/mode', methods=['POST'])
def set_mode():
    mode_id = request.json.get("mode_id")
    drone.change_mode(mode_id)
    print(f"Changed mode to {mode_id}")
    return jsonify({ "mode_id": mode_id }), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)