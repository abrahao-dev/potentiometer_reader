# Potentiometer Reader for Arduino (Two-Wire Configuration)

This simple Arduino project reads values from a potentiometer and displays them in the Serial Monitor. It includes a Python script for data collection and visualization.

## Hardware Requirements

- Arduino Uno (or compatible board)
- Potentiometer (any value, typically 10kΩ works well)
- Jumper wires
- USB cable for Arduino

## Current Circuit Connection (Two-Wire)

1. Connect one pin of the potentiometer to 5V on the Arduino
2. Connect another pin to Analog pin A0 on the Arduino

## Current Circuit Diagram (Two-Wire)

```
Arduino Uno    Potentiometer
-----------    -------------
     5V  -------- Pin 1
     A0  -------- Pin 2
```

## Recommended Circuit Connection (Three-Wire)

For more stable and reliable readings, consider using the standard three-wire configuration:

1. Connect one outer pin of the potentiometer to 5V on the Arduino
2. Connect the other outer pin to GND on the Arduino
3. Connect the middle pin (wiper) to Analog pin A0 on the Arduino

## Recommended Circuit Diagram (Three-Wire)

```
Arduino Uno    Potentiometer
-----------    -------------
     5V  -------- (+) Pin 1
    GND  -------- (-) Pin 3
     A0  -------- (W) Pin 2 (Middle/Wiper)
```

## How to Use the Arduino Sketch

1. Connect the Arduino to your computer via USB
2. Upload the sketch to your Arduino
3. Open the Serial Monitor (Tools > Serial Monitor)
4. Set the baud rate to 9600
5. Turn the potentiometer knob to see the values change in real-time

## What You'll See in the Serial Monitor

The Serial Monitor will display:
- Raw analog value (0-1023)
- Calculated voltage (0-5V)

These values update every 500 milliseconds.

## Using the Python Data Collection Script

The included Python script (`script.py`) provides advanced data collection and visualization capabilities.

### Prerequisites

```bash
pip install pyserial matplotlib
```

### Basic Usage

```bash
python script.py
```

The script will automatically detect your Arduino port and start collecting data.

### Advanced Options

```bash
python script.py --port /dev/ttyUSB0 --baud 9600 --output my_data.csv --plot
```

- `--port`: Specify the serial port manually (e.g., COM3 on Windows, /dev/ttyUSB0 on Linux)
- `--baud`: Set the baud rate (default: 9600)
- `--output`: Specify a custom output filename (default: potentiometer_data_TIMESTAMP.csv)
- `--plot`: Enable real-time plotting of voltage readings

### Data Format

The script saves data in CSV format with the following columns:
- Timestamp: Unix timestamp of the reading
- Elapsed Time (s): Time in seconds since data collection started
- Voltage (V): Voltage reading from the potentiometer (0-5V)

### Real-time Visualization

When using the `--plot` option, the script displays a real-time graph of voltage readings over time. The graph automatically adjusts to show the most recent 30 seconds of data.

### Stopping Data Collection

Press `Ctrl+C` in the terminal to stop data collection. The script will display a summary of the collected data before exiting.
