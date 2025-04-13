# Project Name: Hand-Sync-Arduino

## Project Summary
Hand-Sync-Arduino is an Arduino-based robotic hand project that synchronizes with real hand movements using computer vision libraries. This project calculates the hand's grip angle in real-time and transmits it to the Arduino to control the servo motors of the robotic hand. It also supports tracking hand movements remotely using an IP camera.

## Requirements
- **Hardware**
  - Arduino Uno (or compatible board)
  - Servo motors
  - IP camera (optional)
- **Software**
  - Python 3.12 or higher
  - Libraries: OpenCV, MediaPipe, PySerial

## Project Structure
### 1. [src/main.cpp](src/main.cpp)
Firmware code running on the Arduino. Key functionalities include:
- Receiving the hand's grip angle via serial communication from the computer.
- Controlling the servo motors to synchronize the robotic hand's movements with the received angle.
- Validating input values and ensuring smooth servo motor movements.

### 2. [hand-control/control.py](hand-control/hand_control/control.py)
Python-based control code. Key functionalities include:
- Capturing real-time hand images using a camera (webcam or IP camera).
- Extracting hand landmarks using MediaPipe and calculating finger angles.
- Transmitting the calculated grip angle to the Arduino via serial communication.
- Supporting remote operation using an IP camera.


## Notes
- For IP camera usage, install the IP Webcam app (Android) on your smartphone to provide a camera stream.
- The serial communication speed between the Arduino and the computer is set to 9600bps.
