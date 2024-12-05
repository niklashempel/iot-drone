from flask import Flask, request, jsonify, render_template
from drone import Drone

app = Flask(__name__)

drone = Drone()
drone.connect()

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
        return jsonify(drone.arm()), 200
    elif command == "disarm":
        return jsonify(drone.disarm()), 200
    elif command == "takeoff":
        return jsonify(drone.takeoff()), 200
    elif command == "land":
        return jsonify(drone.land()), 200
    else:
        return jsonify({"error": "Unsupported command"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)