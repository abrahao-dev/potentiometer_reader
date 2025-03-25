#!/usr/bin/env python3
"""
Potentiometer Reader Data Collector

This script reads data from an Arduino running the potentiometer_reader sketch,
saves the data to a CSV file, and provides options for real-time visualization.

Usage:
    python script.py [--port PORT] [--baud BAUD] [--output FILENAME] [--plot]
"""

import serial
import csv
import time
import argparse
import os
import sys
from datetime import datetime
import re

# Optional matplotlib import for plotting
try:
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

def find_arduino_port():
    """Attempt to automatically find the Arduino port."""
    import serial.tools.list_ports
    
    # Common Arduino identifiers
    arduino_identifiers = [
        "Arduino", "CH340", "FTDI", "usbserial", "usbmodem", "wchusbserial"
    ]
    
    ports = list(serial.tools.list_ports.comports())
    
    for port in ports:
        for identifier in arduino_identifiers:
            if identifier.lower() in port.description.lower() or identifier.lower() in port.device.lower():
                return port.device
    
    return None

def parse_arduino_data(line):
    """Parse the data coming from Arduino."""
    # Extract voltage from the line (assuming format like "Raw value: 123 Voltage: 2.45 V")
    voltage_match = re.search(r'Voltage:\s+(\d+\.\d+)', line)
    
    if voltage_match:
        voltage = float(voltage_match.group(1))
        timestamp = time.time()
        return timestamp, voltage
    
    return None, None

def setup_plotting():
    """Setup real-time plotting if matplotlib is available."""
    if not MATPLOTLIB_AVAILABLE:
        print("Matplotlib not available. Install with: pip install matplotlib")
        return None, None, None
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title('Potentiometer Readings')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Voltage (V)')
    ax.grid(True)
    
    # Initialize empty lists for data
    times = []
    voltages = []
    
    # Create line object
    line, = ax.plot([], [], 'b-')
    
    # Set up plot to be animated
    def init():
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 5.5)
        return line,
    
    def update(frame):
        if times and voltages:
            # Update the line with new data
            line.set_data(times, voltages)
            
            # Adjust x-axis limits to show the last 30 seconds of data
            if len(times) > 1:
                start_time = times[0]
                current_time = times[-1]
                ax.set_xlim(max(0, current_time - start_time - 30), current_time - start_time + 1)
                
                # Adjust y-axis to fit the data with some padding
                min_voltage = min(voltages)
                max_voltage = max(voltages)
                padding = (max_voltage - min_voltage) * 0.1 if max_voltage > min_voltage else 0.5
                ax.set_ylim(max(0, min_voltage - padding), min(5.5, max_voltage + padding))
        
        return line,
    
    # Create animation
    ani = FuncAnimation(fig, update, init_func=init, interval=100, blit=True)
    
    return fig, (times, voltages), ani

def main():
    """Main function to run the data collection."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Arduino Potentiometer Data Collector')
    parser.add_argument('--port', help='Serial port (e.g., /dev/ttyUSB0, COM3)')
    parser.add_argument('--baud', type=int, default=9600, help='Baud rate (default: 9600)')
    parser.add_argument('--output', default=None, help='Output CSV filename (default: potentiometer_data_TIMESTAMP.csv)')
    parser.add_argument('--plot', action='store_true', help='Enable real-time plotting (requires matplotlib)')
    
    args = parser.parse_args()
    
    # Determine port
    port = args.port
    if not port:
        port = find_arduino_port()
        if not port:
            print("Error: Could not automatically find Arduino port. Please specify with --port.")
            print("Available ports:")
            import serial.tools.list_ports
            for p in serial.tools.list_ports.comports():
                print(f"  {p.device} - {p.description}")
            return 1
    
    # Determine output filename
    if not args.output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"potentiometer_data_{timestamp}.csv"
    else:
        output_filename = args.output
    
    # Setup plotting if requested
    plot_data = None
    if args.plot:
        if MATPLOTLIB_AVAILABLE:
            fig, plot_data, ani = setup_plotting()
            plt.ion()  # Turn on interactive mode
            plt.show(block=False)
        else:
            print("Warning: Plotting requested but matplotlib is not available.")
            print("Install matplotlib with: pip install matplotlib")
    
    # Connect to Arduino
    print(f"Connecting to Arduino on {port} at {args.baud} baud...")
    try:
        arduino = serial.Serial(port, args.baud, timeout=2)
        # Wait for connection to stabilize
        time.sleep(2)
        print("Connection established.")
    except serial.SerialException as e:
        print(f"Error connecting to Arduino: {e}")
        return 1
    
    # Create and open CSV file
    try:
        with open(output_filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Elapsed Time (s)", "Voltage (V)"])
            
            print(f"Data collection started. Saving to {output_filename}")
            print("Press Ctrl+C to stop collection.")
            
            start_time = time.time()
            
            try:
                while True:
                    try:
                        line = arduino.readline().decode('utf-8', errors='replace').strip()
                        if line:
                            timestamp, voltage = parse_arduino_data(line)
                            
                            if timestamp and voltage is not None:
                                elapsed = timestamp - start_time
                                
                                # Write to CSV
                                writer.writerow([timestamp, round(elapsed, 2), voltage])
                                file.flush()
                                
                                # Print to console
                                print(f"Time: {elapsed:.2f}s, Voltage: {voltage:.2f}V")
                                
                                # Update plot if enabled
                                if plot_data:
                                    times, voltages = plot_data
                                    times.append(elapsed)
                                    voltages.append(voltage)
                                    if len(times) > 1000:  # Limit data points to avoid memory issues
                                        times.pop(0)
                                        voltages.pop(0)
                                    plt.pause(0.01)  # Update the plot
                            else:
                                print(f"Raw data: {line}")
                    except UnicodeDecodeError:
                        print("Warning: Received invalid data from Arduino.")
                        continue
                    
            except KeyboardInterrupt:
                print("\nData collection stopped by user.")
            
            # Final statistics
            if os.path.exists(output_filename):
                with open(output_filename, 'r') as f:
                    line_count = sum(1 for _ in f) - 1  # Subtract header
                print(f"\nCollection summary:")
                print(f"- Data points collected: {line_count}")
                print(f"- Duration: {time.time() - start_time:.2f} seconds")
                print(f"- Data saved to: {output_filename}")
    
    except Exception as e:
        print(f"Error during data collection: {e}")
    finally:
        # Clean up
        arduino.close()
        print("Serial connection closed.")
        
        # If plotting was enabled, keep the plot window open
        if args.plot and MATPLOTLIB_AVAILABLE:
            print("Keeping plot window open. Close it to exit.")
            plt.ioff()
            plt.show()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
