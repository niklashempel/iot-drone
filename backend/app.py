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

@app.route('/arm', methods=['POST'])
def arm():
    drone.arm()
    return jsonify(), 200

@app.route('/disarm', methods=['POST'])
def disarm():
    drone.disarm()
    return jsonify(), 200

@app.route('/takeoff', methods=['POST'])
def takeoff():
    return jsonify(drone.takeoff()), 200

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
    print(f"Changing mode to {mode_id}")
    drone.change_mode(mode_id)
    print(f"Changed mode to {mode_id}")
    return jsonify({ "mode_id": mode_id }), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)