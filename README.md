# IoT Drone

## Description

This repository contains the code for the IoT Drone project. The project is a drone that can be controlled via a web interface. The drone is a Pixhawk 2.4.8. The web interface is a Flask server that communicates with the drone via MAVLink.
This repository includes `ArduCopter` as a submodule. This way, we can use the SITL (Software In The Loop) to test the drone's behavior without having to fly it.

## Quick Start

Clone the repository including the submodules:

```sh
git clone --recurse-submodules
cd iot-drone
```

Init virtual environment:

```sh
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

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
