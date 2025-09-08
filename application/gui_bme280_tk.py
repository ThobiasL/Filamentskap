#!/usr/bin/env python3
"""
GUI for displaying temperature and humidity from two BME280 sensors.

- Polls two BME280 sensors (default I2C addresses 0x77 and 0x76).
- Shows each sensor's temperature & humidity and the averages.
- Updates every 2 seconds.
- Uses the existing adapters/ports if available, otherwise falls back to local files.
"""

import sys
import os
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox

# --- Import helpers to support both "adapters/ports" layout and flat files ---
def _try_imports():
    sensor_cls = None
    avg_fn = None

    # 1) Try package-style imports
    try:
        from adapters.BME280_adapter import BME280Sensor  # type: ignore
        from ports.TempAndHumidSensor_port import average  # type: ignore
        sensor_cls = BME280Sensor
        avg_fn = average
        return sensor_cls, avg_fn
    except Exception:
        pass

    # 2) Try flat-file imports
    try:
        # If the files are in the same folder as this script, make sure it's on sys.path
        here = os.path.abspath(os.path.dirname(__file__))
        if here not in sys.path:
            sys.path.insert(0, here)

        from BME280_adapter import BME280Sensor  # type: ignore
        try:
            # Prefer the ports helper if present
            from ports.TempAndHumidSensor_port import average  # type: ignore
        except Exception:
            from TempAndHumidSensor_port import average  # type: ignore

        sensor_cls = BME280Sensor
        avg_fn = average
        return sensor_cls, avg_fn
    except Exception as e:
        raise ImportError(
            "Kunne ikke importere BME280-adapteren og/eller average()-funksjonen. "
            "Sørg for at filene er tilgjengelige, og at 'bme280' og 'smbus2' er installert.\n"
            f"Original feil: {e}"
        )

BME280Sensor, average = _try_imports()


class SensorReader:
    '''\"\"\"Background polling of two BME280 sensors.\"\"\"'''

    def __init__(self, addr1=0x77, addr2=0x76, interval=2.0):
        self.addr1 = addr1
        self.addr2 = addr2
        self.interval = float(interval)

        # Instantiate sensors
        self.s1 = BME280Sensor(self.addr1)
        self.s2 = BME280Sensor(self.addr2)

        # State
        self._stop = threading.Event()
        self.latest = {
            "t1": None, "h1": None,
            "t2": None, "h2": None,
            "t_avg": None, "h_avg": None,
            "error": None,
        }

        self._thread = threading.Thread(target=self._loop, daemon=True)

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop.set()
        # Best-effort: BME280_adapter doesn't expose a close() method, so nothing to close explicitly.

    def _loop(self):
        while not self._stop.is_set():
            try:
                t1 = round(float(self.s1.read_temperature()), 1)
                t2 = round(float(self.s2.read_temperature()), 1)
                h1 = round(float(self.s1.read_humidity()), 1)
                h2 = round(float(self.s2.read_humidity()), 1)

                t_avg = round(float(average(t1, t2)), 1)
                h_avg = round(float(average(h1, h2)), 1)

                self.latest.update({
                    "t1": t1, "h1": h1,
                    "t2": t2, "h2": h2,
                    "t_avg": t_avg, "h_avg": h_avg,
                    "error": None,
                })
            except Exception as e:
                self.latest["error"] = str(e)

            time.sleep(self.interval)


class App(tk.Tk):
    def __init__(self, poll_interval_ms=500):
        super().__init__()
        self.title("Temp & Humidity (BME280)")
        self.geometry("520x280")
        self.resizable(False, False)

        # Styling
        try:
            self.tk.call("tk", "scaling", 1.25)
        except Exception:
            pass

        self.style = ttk.Style(self)
        self.style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
        self.style.configure("Value.TLabel", font=("Segoe UI", 14))
        self.style.configure("Unit.TLabel", font=("Segoe UI", 10), foreground="#555")
        self.style.configure("Status.TLabel", font=("Segoe UI", 10), foreground="#a00")

        # Header
        header = ttk.Label(self, text="Temperatur & Fuktighet", style="Title.TLabel")
        header.pack(pady=(14, 8))

        # Grid for values
        container = ttk.Frame(self, padding=16)
        container.pack(fill="both", expand=True)

        # Column headers
        ttk.Label(container, text="Sensor", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, padx=6, pady=4, sticky="w")
        ttk.Label(container, text="Temperatur (°C)", font=("Segoe UI", 11, "bold")).grid(row=0, column=1, padx=6, pady=4)
        ttk.Label(container, text="Fuktighet (%)", font=("Segoe UI", 11, "bold")).grid(row=0, column=2, padx=6, pady=4)

        # Rows for sensor 1 & 2
        self.t1_var = tk.StringVar(value="—")
        self.h1_var = tk.StringVar(value="—")
        self.t2_var = tk.StringVar(value="—")
        self.h2_var = tk.StringVar(value="—")
        self.ta_var = tk.StringVar(value="—")
        self.ha_var = tk.StringVar(value="—")

        ttk.Label(container, text="Sensor 1").grid(row=1, column=0, padx=6, pady=6, sticky="w")
        ttk.Label(container, textvariable=self.t1_var, style="Value.TLabel").grid(row=1, column=1, padx=6, pady=6)
        ttk.Label(container, textvariable=self.h1_var, style="Value.TLabel").grid(row=1, column=2, padx=6, pady=6)

        ttk.Label(container, text="Sensor 2").grid(row=2, column=0, padx=6, pady=6, sticky="w")
        ttk.Label(container, textvariable=self.t2_var, style="Value.TLabel").grid(row=2, column=1, padx=6, pady=6)
        ttk.Label(container, textvariable=self.h2_var, style="Value.TLabel").grid(row=2, column=2, padx=6, pady=6)

        ttk.Separator(container).grid(row=3, column=0, columnspan=3, sticky="ew", pady=(8, 4))

        ttk.Label(container, text="Gjennomsnitt", font=("Segoe UI", 11, "bold")).grid(row=4, column=0, padx=6, pady=6, sticky="w")
        ttk.Label(container, textvariable=self.ta_var, style="Value.TLabel").grid(row=4, column=1, padx=6, pady=6)
        ttk.Label(container, textvariable=self.ha_var, style="Value.TLabel").grid(row=4, column=2, padx=6, pady=6)

        # Status line
        self.status_var = tk.StringVar(value="Starter sensorer…")
        ttk.Label(self, textvariable=self.status_var, style="Status.TLabel").pack(pady=(0, 8))

        # Reader + schedule UI updates
        self.reader = SensorReader()
        self.reader.start()

        self.poll_interval_ms = int(poll_interval_ms)
        self.after(self.poll_interval_ms, self._refresh)

        # Close handling
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _refresh(self):
        data = self.reader.latest
        if data.get("error"):
            self.status_var.set(f"Feil: {data['error']}")
        else:
            self.status_var.set("Oppdatert")
        # Update labels if values exist
        def fmt(v):
            return "—" if v is None else f"{v:.1f}"

        self.t1_var.set(fmt(data.get("t1")))
        self.h1_var.set(fmt(data.get("h1")))
        self.t2_var.set(fmt(data.get("t2")))
        self.h2_var.set(fmt(data.get("h2")))
        self.ta_var.set(fmt(data.get("t_avg")))
        self.ha_var.set(fmt(data.get("h_avg")))

        self.after(self.poll_interval_ms, self._refresh)

    def _on_close(self):
        try:
            self.reader.stop()
        finally:
            self.destroy()


def main():
    app = App(poll_interval_ms=500)
    app.mainloop()


if __name__ == "__main__":
    main()
