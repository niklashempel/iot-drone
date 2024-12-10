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

Init ardupilot (follow https://ardupilot.org/dev/docs/building-the-code.html#building-the-code)

For Linux:

```sh
# deactivate the virtual environment if you are in it
deactivate
cd ardupilot
Tools/environment_install/install-prereqs-ubuntu.sh -y
./waf configure --board fmuv3
./waf copter
```

Init virtual environment:

```sh
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Start services

```sh
# make sure you are at root level of the repository

./ardupilot/Tools/autotest/sim_vehicle.py -v copter --console --map -w --out 127.0.0.1:14550 --out 127.0.0.1:14551 &
./mavlink2rest/mavlink2rest-x86_64-unknown-linux-musl -c udpin:0.0.0.0:14551
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
