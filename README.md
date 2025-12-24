# Motor Example Using PyModbus
## Introduction
This project provides a Python interface for controlling BLDC servo motors via **pymodbus**. It supports position and speed control, as well as register-based data retrieval.

The code includes a preliminary implementation of getters and setters for essential motor data, serving as a template for further expansion.

## Features
* **Modbus RTU Communication**: Built on top of `pymodbus` for reliable serial communication.
* **High-Level Abstraction**:
    * Automatic conversion between Encoder Counts and Degrees.
    * Easy-to-use API for Speed (`deg/s`) and Torque (`Nm`) readings.
* **Comprehensive Control**:
    * Position Control (Trapezoidal Ramp & Direct).
    * Velocity & Acceleration configuration.
    * PID Gain tuning.
* **Robust Logging**: Integrated `logging` module for debugging serial interactions and register states.
* **Safety**: Includes error handling for Modbus connection issues.

## Hardware Setup
- **Motor**: Simplex Motion SC020B
- **Communication Protocol**: Modbus RTU
- **Connection**: USB to RS485 Adapter

## Installation
**Required Library**
* `pymodbus` (Version 3.8.6)

To install the dependencies, run:

```bash
pip install pymodbus==3.8.6
```

## File Structure
- **`simplexMotor.py`**: The main driver class. Handles connections, read/write logic, and unit conversions.
- **`reg_map.py`**: Defines constants for Register Addresses and Mode values.
- **`simplex_example.py`**: An interactive CLI tool to test motor position control. Users can input a target value to move the motor to that position (in degrees).

## Code Overview
The `SimplexMotor` class in `simplexMotor.py` is organized into three main functional areas:

- **Getters**: Retrieve motor parameters and real-time data (e.g., position, speed), handling necessary unit conversions.
- **Setters**: Configure motor settings and send control commands (e.g., target position, operation mode).
- **Internal Helpers**: Handle connection validation, error processing, and formatted logging.


## Others
For a detailed breakdown of the process and development history, check out the **HackMD note**:
https://hackmd.io/@zhewei0113/H1T6LJoZbg