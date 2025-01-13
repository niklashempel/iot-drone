# IoT Drone

## Description

This repository contains the code for the IoT Drone project. The project is a drone that can be controlled via a web interface. The drone is a Pixhawk 2.4.8. The web interface is a Flask server that communicates with the drone via MAVLink.

## Pre-requisites

- [Docker](https://docs.docker.com/get-docker/)
- [Python 3](https://www.python.org/downloads/)
- [MAVProxy](https://ardupilot.org/mavproxy/docs/getting_started/download_and_installation.html)

⚠️ After installing MAVProxy, we have to install a python package, that is required for the MQTT module. To do so, run the following command: `pip3 install paho-mqtt<2`

## Quick Start

Depending on whether we use a real drone or a simulated drone, we may can omit starting the simulator SITL.

### Real drone

Start MAVProxy

```sh
mavproxy.py --baudrate 57600 --console --out=udp:127.0.0.1:14550 --cmd "module load mqtt" --cmd "mqtt set prefix iotdrone" --cmd "mqtt connect"
```

Start the Flask server

```sh
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Start MQTT Server and Node-RED

```sh
docker compose up mqtt node-red
```

### Simulated drone

Start MQTT Server and SITL

```sh
docker compose up mqtt ardupilot-sitl
```

Start MAVProxy

```sh
mavproxy.py --master=tcp:127.0.0.1:5760 --baudrate 57600 --console --out=udp:127.0.0.1:14550 --cmd "module load mqtt" --cmd "mqtt set prefix iotdrone" --cmd "mqtt connect"
```

Start the Flask server

```sh
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Start Node-RED dashboard

```sh
docker compose up node-red
```

Open http://localhost:1880/dashboard in a browser.

## MAVLink Communication

Fly up and down:

```sh
mode stabilize
arm throttle
mode *guided*
takeoff 10
mode alt_hold
land
```

Status:

```sh
status
```
