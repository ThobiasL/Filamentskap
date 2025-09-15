#!/usr/bin/env python3
"""
Data Bridge for Filament Storage Monitor
File: Filamentskap/bridge/data_bridge.py

This program acts as a bridge between main.py and gui_main.py
by providing shared data through JSON files and optional socket communication.
"""

import sys
import os
import json
import time
import threading
import socket
from datetime import datetime
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core')))

try:
    from adapters.BME280_adapter import BME280Sensor, average
    from adapters.ledstrip_adapter import LEDStripAdapter

    SENSORS_AVAILABLE = True
except ImportError:
    print("Warning: Hardware adapters not available. Running in simulation mode.")
    SENSORS_AVAILABLE = False


class SensorSimulator:
    """Simulator for testing without actual hardware"""

    def __init__(self, base_temp=22.0, base_humidity=45.0):
        self.base_temp = base_temp
        self.base_humidity = base_humidity
        import random
        self.random = random

    def read_temperature(self):
        return self.base_temp + self.random.uniform(-2.0, 3.0)

    def read_humidity(self):
        return self.base_humidity + self.random.uniform(-10.0, 15.0)

    def close(self):
        pass


class DataBridge:
    """Main data bridge class"""

    def __init__(self):
        self.running = True
        self.data_file = None
        self.socket_server = None
        self.setup_paths()
        self.setup_sensors()
        self.setup_variables()

    def setup_paths(self):
        """Setup file paths for data sharing"""
        self.bridge_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(self.bridge_dir)

        # Create data directory if it doesn't exist
        self.data_dir = os.path.join(self.project_root, 'data')
        Path(self.data_dir).mkdir(exist_ok=True)

        # Data file path
        self.data_file = os.path.join(self.data_dir, 'sensor_data.json')

        print(f"Data bridge initialized")
        print(f"Data file: {self.data_file}")

    def setup_sensors(self):
        """Initialize sensors or simulators"""
        if SENSORS_AVAILABLE:
            try:
                self.sensor1 = BME280Sensor(0x77)
                self.sensor2 = BME280Sensor(0x76)
                self.ledstrip = LEDStripAdapter(17, pin=18)
                self.ledstrip.clear()
                self.ledstrip.set_color((255, 255, 255))
                print("✅ Hardware sensors initialized successfully")
            except Exception as e:
                print(f"⚠️  Failed to initialize hardware: {e}")
                print("🔄 Falling back to simulation mode")
                self.setup_simulators()
        else:
            self.setup_simulators()

    def setup_simulators(self):
        """Setup sensor simulators for testing"""
        self.sensor1 = SensorSimulator(22.0, 45.0)
        self.sensor2 = SensorSimulator(23.0, 47.0)
        self.ledstrip = None
        print("🎮 Running in simulation mode")

    def setup_variables(self):
        """Initialize variables"""
        self.humidity_limit = 60.0
        self.warning_active = False
        self.update_interval = 2.0  # seconds

        # LED warning variables
        self.normal_led_state = (255, 255, 255)
        self.warning_led_state = (255, 0, 0)
        self.led_warning_signal = False
        self.led_timer = 0
        self.led_timer_limit = 20
        self.manual_override = False

    def read_sensors(self):
        """Read data from sensors and return structured data"""
        try:
            temp1 = round(self.sensor1.read_temperature(), 1)
            temp2 = round(self.sensor2.read_temperature(), 1)
            humidity1 = round(self.sensor1.read_humidity(), 1)
            humidity2 = round(self.sensor2.read_humidity(), 1)

            avg_temp = round(average(temp1, temp2), 1)
            avg_humidity = round(average(humidity1, humidity2), 1)

            data = {
                'timestamp': datetime.now().isoformat(),
                'sensor1': {
                    'temperature': temp1,
                    'humidity': humidity1
                },
                'sensor2': {
                    'temperature': temp2,
                    'humidity': humidity2
                },
                'averages': {
                    'temperature': avg_temp,
                    'humidity': avg_humidity
                },
                'status': {
                    'humidity_warning': avg_humidity > self.humidity_limit,
                    'led_warning_active': self.led_warning_signal,
                    'system_status': 'operational'
                }
            }

            return data

        except Exception as e:
            print(f"❌ Error reading sensors: {e}")
            return None

    def update_led_warning(self, avg_humidity):
        """Handle LED warning logic"""
        if not self.ledstrip or self.manual_override:
            return

        if avg_humidity > self.humidity_limit and not self.led_warning_signal:
            self.ledstrip.clear()
            self.ledstrip.set_color(self.warning_led_state)
            self.led_warning_signal = True
            self.led_timer = 0
            print(f"🚨 Humidity warning activated: {avg_humidity}%")

        elif avg_humidity < self.humidity_limit and self.led_warning_signal:
            if self.led_timer > self.led_timer_limit:
                self.ledstrip.clear()
                self.ledstrip.set_color(self.normal_led_state)
                self.led_warning_signal = False
                self.led_timer = 0
                print(f"✅ Humidity warning cleared: {avg_humidity}%")
            else:
                self.led_timer += 1

    def write_data_file(self, data):
        """Write data to JSON file for GUI to read"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Error writing data file: {e}")
            return False

    def setup_socket_server(self, port=8888):
        """Setup socket server for real-time communication (optional)"""
        try:
            self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket_server.bind(('localhost', port))
            self.socket_server.listen(5)
            self.socket_server.settimeout(1.0)  # Non-blocking
            print(f"🌐 Socket server listening on port {port}")
            return True
        except Exception as e:
            print(f"⚠️  Socket server setup failed: {e}")
            self.socket_server = None
            return False

    def handle_socket_connections(self):
        """Handle incoming socket connections"""
        if not self.socket_server:
            return

        while self.running:
            try:
                client_socket, address = self.socket_server.accept()
                # Send latest data to client
                if hasattr(self, 'latest_data') and self.latest_data:
                    data_str = json.dumps(self.latest_data)
                    client_socket.send(data_str.encode())
                client_socket.close()
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"Socket error: {e}")
                break

    def main_loop(self):
        """Main data collection and distribution loop"""
        print("🚀 Starting data bridge main loop...")

        # Start socket server in background thread if enabled
        socket_enabled = self.setup_socket_server()
        if socket_enabled:
            socket_thread = threading.Thread(target=self.handle_socket_connections, daemon=True)
            socket_thread.start()

        iteration = 0
        while self.running:
            try:
                # Read sensor data
                data = self.read_sensors()
                if data:
                    # Store for socket server
                    self.latest_data = data

                    # Write to file for GUI
                    if self.write_data_file(data):
                        # Update LED warning
                        avg_humidity = data['averages']['humidity']
                        self.update_led_warning(avg_humidity)

                        # Print status every 10 iterations (20 seconds)
                        iteration += 1
                        if iteration % 10 == 0:
                            print(f"📊 Bridge active - Temp: {data['averages']['temperature']}°C, "
                                  f"Humidity: {avg_humidity}% [{data['timestamp']}]")
                else:
                    print("⚠️  Failed to read sensor data")

                time.sleep(self.update_interval)

            except KeyboardInterrupt:
                print("\n🛑 Shutdown requested...")
                break
            except Exception as e:
                print(f"❌ Main loop error: {e}")
                time.sleep(self.update_interval)

        self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        print("🧹 Cleaning up data bridge...")
        self.running = False

        # Close sensors
        try:
            if hasattr(self, 'sensor1'):
                self.sensor1.close()
            if hasattr(self, 'sensor2'):
                self.sensor2.close()
            if hasattr(self, 'ledstrip') and self.ledstrip:
                self.ledstrip.clear()
        except Exception as e:
            print(f"Sensor cleanup error: {e}")

        # Close socket server
        if self.socket_server:
            try:
                self.socket_server.close()
            except Exception as e:
                print(f"Socket cleanup error: {e}")

        print("✅ Data bridge cleanup complete")


def main():
    """Main entry point"""
    print("=" * 50)
    print("🌉 FILAMENT STORAGE MONITOR - DATA BRIDGE")
    print("=" * 50)

    # Create and run the data bridge
    bridge = DataBridge()

    try:
        bridge.main_loop()
    except KeyboardInterrupt:
        print("\n🛑 Data bridge interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        bridge.cleanup()


if __name__ == "__main__":
    main()