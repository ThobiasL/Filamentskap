#!/usr/bin/env python3
"""
GUI Program for Raspberry Pi - Temperature and Humidity Monitor
File: Filamentskap/application/gui_main.py
"""

import sys
import os
import tkinter as tk
from tkinter import ttk
import threading
import time
import math

# Add the parent directory to the Python path to access core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core')))

try:
    from adapters.BME280_adapter import BME280Sensor, average
    from adapters.ledstrip_adapter import LEDStripAdapter

    SENSORS_AVAILABLE = True
except ImportError:
    print("Warning: Hardware adapters not available. Running in simulation mode.")
    SENSORS_AVAILABLE = False


class HexagonWidget:
    """Custom hexagon widget for displaying sensor data"""

    def __init__(self, canvas, x, y, size, title, color="#4CAF50"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.title = title
        self.color = color
        self.value = "0.0"
        self.unit = ""
        self.create_hexagon()

    def create_hexagon(self):
        """Create a hexagonal shape on the canvas"""
        points = []
        for i in range(6):
            angle = math.pi / 3 * i
            point_x = self.x + self.size * math.cos(angle)
            point_y = self.y + self.size * math.sin(angle)
            points.extend([point_x, point_y])

        # Create hexagon shape
        self.hexagon_id = self.canvas.create_polygon(
            points,
            fill=self.color,
            outline="#2E7D32",
            width=3,
            tags="hexagon"
        )

        # Create title text
        self.title_id = self.canvas.create_text(
            self.x, self.y - 20,
            text=self.title,
            font=("Arial", 10, "bold"),
            fill="white",
            tags="hexagon"
        )

        # Create value text
        self.value_id = self.canvas.create_text(
            self.x, self.y + 5,
            text=self.value,
            font=("Arial", 16, "bold"),
            fill="white",
            tags="hexagon"
        )

        # Create unit text
        self.unit_id = self.canvas.create_text(
            self.x, self.y + 25,
            text=self.unit,
            font=("Arial", 8),
            fill="white",
            tags="hexagon"
        )

    def update_value(self, value, unit=""):
        """Update the displayed value and unit"""
        self.value = f"{value:.1f}"
        self.unit = unit
        self.canvas.itemconfig(self.value_id, text=self.value)
        self.canvas.itemconfig(self.unit_id, text=self.unit)

    def update_color(self, color):
        """Update the hexagon color"""
        self.color = color
        self.canvas.itemconfig(self.hexagon_id, fill=color)


class SensorSimulator:
    """Simulator for testing without actual hardware"""

    def __init__(self, base_temp=22.0, base_humidity=45.0):
        self.base_temp = base_temp
        self.base_humidity = base_humidity
        import random
        self.random = random

    def read_temperature(self):
        # Simulate temperature variation
        return self.base_temp + self.random.uniform(-2.0, 3.0)

    def read_humidity(self):
        # Simulate humidity variation
        return self.base_humidity + self.random.uniform(-10.0, 15.0)

    def close(self):
        pass


class TemperatureHumidityGUI:
    """Main GUI application class"""

    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.setup_sensors()
        self.create_widgets()
        self.start_sensor_thread()

    def setup_window(self):
        """Configure the main window"""
        self.root.title("Filament Storage Monitor")
        self.root.geometry("800x600")
        self.root.configure(bg="#1E1E1E")
        self.root.resizable(True, True)

        # Make window responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def setup_variables(self):
        """Initialize application variables"""
        self.running = True
        self.update_interval = 2.0  # seconds

        # Sensor data variables
        self.temp1 = 0.0
        self.temp2 = 0.0
        self.humidity1 = 0.0
        self.humidity2 = 0.0
        self.avg_temp = 0.0
        self.avg_humidity = 0.0

        # Warning settings
        self.humidity_limit = 60.0
        self.warning_active = False

    def setup_sensors(self):
        """Initialize sensors or simulators"""
        if SENSORS_AVAILABLE:
            try:
                self.sensor1 = BME280Sensor(0x77)
                self.sensor2 = BME280Sensor(0x76)
                self.ledstrip = LEDStripAdapter(17, pin=18)
                self.ledstrip.clear()
                self.ledstrip.set_color((255, 255, 255))
                print("Hardware sensors initialized successfully")
            except Exception as e:
                print(f"Failed to initialize hardware: {e}")
                print("Falling back to simulation mode")
                self.setup_simulators()
        else:
            self.setup_simulators()

    def setup_simulators(self):
        """Setup sensor simulators for testing"""
        self.sensor1 = SensorSimulator(22.0, 45.0)
        self.sensor2 = SensorSimulator(23.0, 47.0)
        self.ledstrip = None
        print("Running in simulation mode")

    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Title
        title_label = tk.Label(
            main_frame,
            text="🌡️ Filament Storage Monitor 💧",
            font=("Arial", 24, "bold"),
            bg="#1E1E1E",
            fg="white"
        )
        title_label.grid(row=0, column=0, pady=20)

        # Canvas for hexagons
        self.canvas = tk.Canvas(
            main_frame,
            bg="#1E1E1E",
            highlightthickness=0
        )
        self.canvas.grid(row=1, column=0, sticky="nsew", pady=10)

        # Status frame
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=2, column=0, sticky="ew", pady=10)
        status_frame.grid_columnconfigure(1, weight=1)

        # Status label
        tk.Label(
            status_frame,
            text="Status:",
            font=("Arial", 12, "bold"),
            bg="#1E1E1E",
            fg="white"
        ).grid(row=0, column=0, padx=(0, 10))

        self.status_label = tk.Label(
            status_frame,
            text="Initializing...",
            font=("Arial", 12),
            bg="#1E1E1E",
            fg="#4CAF50"
        )
        self.status_label.grid(row=0, column=1, sticky="w")

        # Bind canvas resize event
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        # Create hexagon widgets after initial layout
        self.root.after(100, self.create_hexagons)

    def create_hexagons(self):
        """Create hexagonal display widgets"""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            self.root.after(100, self.create_hexagons)
            return

        # Clear existing hexagons
        self.canvas.delete("hexagon")

        # Calculate positions and size
        hex_size = min(canvas_width, canvas_height) // 8
        if hex_size < 30:
            hex_size = 30

        # Position calculations for better layout
        center_x = canvas_width // 2
        center_y = canvas_height // 2

        spacing_x = hex_size * 2.5
        spacing_y = hex_size * 2.2

        # Create individual sensor hexagons (top row)
        positions = [
            (center_x - spacing_x, center_y - spacing_y // 2, "Sensor 1 Temp", "#FF5722"),
            (center_x + spacing_x, center_y - spacing_y // 2, "Sensor 1 Humidity", "#2196F3"),
            (center_x - spacing_x, center_y + spacing_y // 2, "Sensor 2 Temp", "#FF5722"),
            (center_x + spacing_x, center_y + spacing_y // 2, "Sensor 2 Humidity", "#2196F3"),
        ]

        # Average hexagons (center)
        avg_positions = [
            (center_x - spacing_x // 2, center_y, "Avg Temp", "#4CAF50"),
            (center_x + spacing_x // 2, center_y, "Avg Humidity", "#009688"),
        ]

        # Create hexagon widgets
        self.hexagons = []

        # Individual sensors
        for x, y, title, color in positions:
            hex_widget = HexagonWidget(self.canvas, x, y, hex_size, title, color)
            self.hexagons.append(hex_widget)

        # Averages
        for x, y, title, color in avg_positions:
            hex_widget = HexagonWidget(self.canvas, x, y, hex_size * 1.2, title, color)
            self.hexagons.append(hex_widget)

    def on_canvas_resize(self, event):
        """Handle canvas resize event"""
        self.root.after(50, self.create_hexagons)

    def read_sensors(self):
        """Read data from sensors"""
        try:
            self.temp1 = round(self.sensor1.read_temperature(), 1)
            self.temp2 = round(self.sensor2.read_temperature(), 1)
            self.humidity1 = round(self.sensor1.read_humidity(), 1)
            self.humidity2 = round(self.sensor2.read_humidity(), 1)

            # Calculate averages
            self.avg_temp = round(average(self.temp1, self.temp2), 1)
            self.avg_humidity = round(average(self.humidity1, self.humidity2), 1)

            return True
        except Exception as e:
            print(f"Error reading sensors: {e}")
            return False

    def update_display(self):
        """Update the hexagonal display with current values"""
        if len(self.hexagons) >= 6:
            # Update individual sensors
            self.hexagons[0].update_value(self.temp1, "°C")
            self.hexagons[1].update_value(self.humidity1, "%")
            self.hexagons[2].update_value(self.temp2, "°C")
            self.hexagons[3].update_value(self.humidity2, "%")

            # Update averages
            self.hexagons[4].update_value(self.avg_temp, "°C")
            self.hexagons[5].update_value(self.avg_humidity, "%")

            # Update humidity warning color
            if self.avg_humidity > self.humidity_limit:
                self.hexagons[5].update_color("#F44336")  # Red for warning
                if not self.warning_active:
                    self.warning_active = True
                    if self.ledstrip:
                        self.ledstrip.clear()
                        self.ledstrip.set_color((255, 0, 0))
            else:
                self.hexagons[5].update_color("#009688")  # Normal color
                if self.warning_active:
                    self.warning_active = False
                    if self.ledstrip:
                        self.ledstrip.clear()
                        self.ledstrip.set_color((255, 255, 255))

    def update_status(self, message, color="#4CAF50"):
        """Update status message"""
        self.status_label.config(text=message, fg=color)

    def sensor_loop(self):
        """Main sensor reading loop (runs in separate thread)"""
        while self.running:
            try:
                if self.read_sensors():
                    # Schedule GUI update in main thread
                    self.root.after(0, self.update_display)
                    self.root.after(0, self.update_status, "Connected - Reading sensors...")
                else:
                    self.root.after(0, self.update_status, "Sensor read error!", "#F44336")

                time.sleep(self.update_interval)
            except Exception as e:
                print(f"Sensor loop error: {e}")
                self.root.after(0, self.update_status, f"Error: {str(e)}", "#F44336")
                time.sleep(self.update_interval)

    def start_sensor_thread(self):
        """Start the sensor reading thread"""
        self.sensor_thread = threading.Thread(target=self.sensor_loop, daemon=True)
        self.sensor_thread.start()
        self.update_status("Starting sensor monitoring...")

    def on_closing(self):
        """Handle application closing"""
        print("Shutting down application...")
        self.running = False

        # Cleanup sensors
        try:
            if hasattr(self, 'sensor1'):
                self.sensor1.close()
            if hasattr(self, 'sensor2'):
                self.sensor2.close()
            if hasattr(self, 'ledstrip') and self.ledstrip:
                self.ledstrip.clear()
        except Exception as e:
            print(f"Cleanup error: {e}")

        self.root.destroy()


def main():
    """Main application entry point"""
    # Create and configure the main window
    root = tk.Tk()

    # Create the application
    app = TemperatureHumidityGUI(root)

    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    # Start the GUI event loop
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        app.on_closing()


if __name__ == "__main__":
    main()