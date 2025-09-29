#!/usr/bin/env python3
"""
Updated GUI Program that reads from Data Bridge
File: Filamentskap/application/gui_main_with_bridge.py
"""

import sys
import os
import tkinter as tk
from tkinter import ttk
import threading
import time
import math
from adapters.sensor_data_bridge_adapter import guiReadingData_adapter
from datetime import datetime


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


class TemperatureHumidityGUIWithBridge:
    """Main GUI application class that reads from data bridge"""

    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.setup_data_source()
        self.create_widgets()
        self.start_data_thread()

    def setup_window(self):
        """Configure the main window"""
        self.root.title("Filament Storage Monitor")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1E1E1E")
        self.root.resizable(True, True)

        # Make window responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def setup_variables(self):
        """Initialize application variables"""
        self.running = True
        self.update_interval = 1.0  # Check for new data every second

        # Sensor data variables
        self.sensor_data = {
            'sensor1': {'temperature': 0.0, 'humidity': 0.0},
            'sensor2': {'temperature': 0.0, 'humidity': 0.0},
            'averages': {'temperature': 0.0, 'humidity': 0.0},
            'status': {'humidity_warning': False, 'system_status': 'disconnected'},
            'timestamp': None
        }

        self.last_update = None
        self.connection_status = "Connecting..."

        # NYTT: unngå race condition når update_display() kjører før hexagoner er laget
        self.hexagons = []

    def setup_data_source(self):
        """Setup data source (adapter)"""
        self.bridge = guiReadingData_adapter()
        print("Data bridge adapter initialisert.")

    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Title with connection status
        title_frame = tk.Frame(main_frame, bg="#1E1E1E")
        title_frame.grid(row=0, column=0, pady=20)

        title_label = tk.Label(
            title_frame,
            text="🌡️ Filament Storage Monitor 💧",
            font=("Arial", 24, "bold"),
            bg="#1E1E1E",
            fg="white"
        )
        title_label.pack()

        self.connection_label = tk.Label(
            title_frame,
            text="🔄 Connecting to data bridge...",
            font=("Arial", 10),
            bg="#1E1E1E",
            fg="#FFA726"
        )
        self.connection_label.pack(pady=(5, 0))

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

        # Status labels
        tk.Label(
            status_frame,
            text="Last Update:",
            font=("Arial", 10, "bold"),
            bg="#1E1E1E",
            fg="white"
        ).grid(row=0, column=0, padx=(0, 10))

        self.last_update_label = tk.Label(
            status_frame,
            text="Never",
            font=("Arial", 10),
            bg="#1E1E1E",
            fg="#4CAF50"
        )
        self.last_update_label.grid(row=0, column=1, sticky="w")

        # Data source info
        tk.Label(
            status_frame,
            text="Data Source:",
            font=("Arial", 10, "bold"),
            bg="#1E1E1E",
            fg="white"
        ).grid(row=1, column=0, padx=(0, 10))

        self.data_source_label = tk.Label(
            status_frame,
            text="Data Bridge (JSON)",
            font=("Arial", 10),
            bg="#1E1E1E",
            fg="#2196F3"
        )
        self.data_source_label.grid(row=1, column=1, sticky="w")

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

        # Calculate larger size for hexagons
        hex_size = min(canvas_width, canvas_height) // 6
        if hex_size < 50:
            hex_size = 50

        # Arrange hexagons in two horizontal rows without overlapping
        center_x = canvas_width // 2
        center_y = canvas_height // 2

        # Calculate spacing to prevent overlap
        spacing_x = hex_size * 2.8
        row_spacing = hex_size * 2.5

        # Top row positions
        top_row_y = center_y - row_spacing // 2
        top_positions = [
            (center_x - spacing_x * 1.5, top_row_y, "Sensor 1 Temp", "#FF5722"),
            (center_x - spacing_x * 0.5, top_row_y, "Avg Temp", "#4CAF50"),
            (center_x + spacing_x * 0.5, top_row_y, "Avg Humidity", "#009688"),
            (center_x + spacing_x * 1.5, top_row_y, "Sensor 1 Humidity", "#2196F3"),
        ]

        # Bottom row positions
        bottom_row_y = center_y + row_spacing // 2
        bottom_positions = [
            (center_x - spacing_x, bottom_row_y, "Sensor 2 Temp", "#FF5722"),
            (center_x + spacing_x, bottom_row_y, "Sensor 2 Humidity", "#2196F3"),
        ]

        # Create hexagon widgets
        self.hexagons = []

        # Top row hexagons
        for x, y, title, color in top_positions:
            if "Avg" in title:
                hex_widget = HexagonWidget(self.canvas, x, y, hex_size * 1.3, title, color)
            else:
                hex_widget = HexagonWidget(self.canvas, x, y, hex_size, title, color)
            self.hexagons.append(hex_widget)

        # Bottom row hexagons
        for x, y, title, color in bottom_positions:
            hex_widget = HexagonWidget(self.canvas, x, y, hex_size, title, color)
            self.hexagons.append(hex_widget)

    def on_canvas_resize(self, event):
        """Handle canvas resize event"""
        self.root.after(50, self.create_hexagons)

    def read_data_from_bridge(self):
        """Read data via Sensor Data Bridge adapter"""
        try:
            values = self.bridge.readData()
            if values is None:
                return None

            # Hvis dokumentet etter hvert returnerer dict direkte, støtt begge formater:
            if isinstance(values, dict):
                # sikre at obligatoriske felt finnes; legg til status hvis mangler
                values.setdefault('status', {'humidity_warning': False, 'system_status': 'operational'})
                values.setdefault('timestamp', datetime.now().isoformat())
                return values

            # Ellers: mappe liste → dict-formatet GUI-et forventer
            return self._values_to_sensor_dict(values)

        except Exception as e:
            print(f"Error reading from adapter: {e}")
            return None

    def _values_to_sensor_dict(self, values):
        """Map [t1, t2, t_avg, h1, h2, h_avg] -> GUI sitt dict-format"""
        if not isinstance(values, (list, tuple)) or len(values) != 6:
            raise ValueError("Forventer liste/tuple med 6 verdier fra adapteren")
        t1, t2, t_avg, h1, h2, h_avg = map(float, values)
        return {
            'sensor1': {'temperature': t1, 'humidity': h1},
            'sensor2': {'temperature': t2, 'humidity': h2},
            'averages': {'temperature': t_avg, 'humidity': h_avg},
            'status': {
                'humidity_warning': False,  # behold standard oppførsel
                'system_status': 'operational'  # regnes som tilkoblet når lesing lykkes
            },
            'timestamp': datetime.now().isoformat()
        }

    def update_display(self):
        """Update the hexagonal display with current values"""
        if len(self.hexagons) >= 6 and self.sensor_data:
            # Update hexagons with data from bridge
            sensor1 = self.sensor_data.get('sensor1', {})
            sensor2 = self.sensor_data.get('sensor2', {})
            averages = self.sensor_data.get('averages', {})
            status = self.sensor_data.get('status', {})

            # Top row: [Sensor 1 Temp, Avg Temp, Avg Humidity, Sensor 1 Humidity]
            # Bottom row: [Sensor 2 Temp, Sensor 2 Humidity]
            self.hexagons[0].update_value(sensor1.get('temperature', 0.0), "°C")
            self.hexagons[1].update_value(averages.get('temperature', 0.0), "°C")
            self.hexagons[2].update_value(averages.get('humidity', 0.0), "%")
            self.hexagons[3].update_value(sensor1.get('humidity', 0.0), "%")
            self.hexagons[4].update_value(sensor2.get('temperature', 0.0), "°C")
            self.hexagons[5].update_value(sensor2.get('humidity', 0.0), "%")

            # Update warning color for humidity
            if status.get('humidity_warning', False):
                self.hexagons[2].update_color("#F44336")  # Red for warning
            else:
                self.hexagons[2].update_color("#009688")  # Normal color

    def update_status_display(self):
        """Update connection and status information"""
        if self.last_update:
            time_str = self.last_update.strftime("%H:%M:%S")
            self.last_update_label.config(text=time_str, fg="#4CAF50")

        # Update connection status
        status = self.sensor_data.get('status', {})
        system_status = status.get('system_status', 'unknown')

        if system_status == 'operational':
            self.connection_label.config(
                text="🟢 Connected to Data Bridge",
                fg="#4CAF50"
            )
        else:
            self.connection_label.config(
                text="🔴 Connection Lost",
                fg="#F44336"
            )

    def data_loop(self):
        """Main data reading loop (runs in separate thread)"""
        consecutive_failures = 0
        max_failures = 5

        while self.running:
            try:
                data = self.read_data_from_bridge()

                if data:
                    self.sensor_data = data
                    self.last_update = datetime.now()
                    consecutive_failures = 0

                    # Schedule GUI update in main thread
                    self.root.after(0, self.update_display)
                    self.root.after(0, self.update_status_display)

                else:
                    consecutive_failures += 1
                    if consecutive_failures >= max_failures:
                        self.root.after(0, self.connection_label.config, {
                            'text': '🔴 Data Bridge Not Found',
                            'fg': '#F44336'
                        })

                time.sleep(self.update_interval)

            except Exception as e:
                print(f"Data loop error: {e}")
                consecutive_failures += 1
                time.sleep(self.update_interval)

    def start_data_thread(self):
        """Start the data reading thread"""
        self.data_thread = threading.Thread(target=self.data_loop, daemon=True)
        self.data_thread.start()

    def on_closing(self):
        """Handle application closing"""
        print("Shutting down GUI...")
        self.running = False
        self.root.destroy()


def main():
    """Main application entry point"""
    # Create and configure the main window
    root = tk.Tk()

    # Create the application
    app = TemperatureHumidityGUIWithBridge(root)

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