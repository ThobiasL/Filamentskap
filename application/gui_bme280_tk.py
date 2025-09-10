# Create a Tkinter GUI that imports sensor access **via main.py** (not directly from adapters).
# It expects main.py to export BME280Sensor and average (as in the user's main.py).

from pathlib import Path

code = r'''#!/usr/bin/env python3'''
"""
GUI for displaying temperature and humidity that **imports from main.py**.

- Imports BME280Sensor and average **from main.py**, to ensure all cross-module
  access goes through main.py (as requested).
- Polls two sensors at I2C addresses 0x77 and 0x76.
- Shows each sensor's temperature & humidity and the averages.
- Updates UI every 500 ms.
"""

import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox

# --- Import strictly via main.py ---
try:
    from Filamentskap/core/main import BME280Sensor, average  # <- NOTE: comes through main.py
except Exception as e:
    raise ImportError(
        "Kunne ikke importere nødvendige symboler fra main.py. "
        "Sørg for at main.py eksporterer BME280Sensor og average.\n"
        f"Original feil: {e}"
    )


class SensorReader:
    \"\"\"Background polling of two BME280 sensors (via main.py).\"\"\"

    def __init__(self, addr1=0x77, addr2=0x76, interval=2.0):
        self.addr1 = addr1
        self.addr2 = addr2
        self.interval = float(interval)

        # Instantiate sensors THROUGH main.py exports
        self.s1 = BME280Sensor(self.addr1)
        self.s2 = BME280Sensor(self.addr2)

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
        # Best-effort clean up if adapter exposes close()
        for s in (self.s1, self.s2):
            if hasattr(s, "close"):
                try:
                    s.close()
                except Exception:
                    pass

    def _loop(self):
        while not self._stop.is_set():
            try:
                t1 = float(self.s1.read_temperature())
                t2 = float(self.s2.read_temperature())
                h1 = float(self.s1.read_humidity())
                h2 = float(self.s2.read_humidity())

                t_avg = average(t1, t2)
                h_avg = average(h1, h2)

                self.latest.update({
                    "t1": round(t1, 1), "h1": round(h1, 1),
                    "t2": round(t2, 1), "h2": round(h2, 1),
                    "t_avg": round(t_avg, 1), "h_avg": round(h_avg, 1),
                    "error": None,
                })
            except Exception as e:
                self.latest["error"] = str(e)

            time.sleep(self.interval)


class App(tk.Tk):
    def __init__(self, poll_interval_ms=500):
        super().__init__()
        self.title("Temp & Humidity (via main.py)")
        self.geometry("520x280")
        self.resizable(False, False)

        try:
            self.tk.call("tk", "scaling", 1.25)
        except Exception:
            pass

        style = ttk.Style(self)
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Value.TLabel", font=("Segoe UI", 14))
        style.configure("Status.TLabel", font=("Segoe UI", 10), foreground="#a00")

        # Header
        ttk.Label(self, text="Temperatur & Fuktighet", style="Title.TLabel").pack(pady=(14, 8))

        # Grid
        frame = ttk.Frame(self, padding=16)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Sensor", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, padx=6, pady=4, sticky="w")
        ttk.Label(frame, text="Temperatur (°C)", font=("Segoe UI", 11, "bold")).grid(row=0, column=1, padx=6, pady=4)
        ttk.Label(frame, text="Fuktighet (%)", font=("Segoe UI", 11, "bold")).grid(row=0, column=2, padx=6, pady=4)

        self.t1_var = tk.StringVar(value="—")
        self.h1_var = tk.StringVar(value="—")
        self.t2_var = tk.StringVar(value="—")
        self.h2_var = tk.StringVar(value="—")
        self.ta_var = tk.StringVar(value="—")
        self.ha_var = tk.StringVar(value="—")

        ttk.Label(frame, text="Sensor 1").grid(row=1, column=0, padx=6, pady=6, sticky="w")
        ttk.Label(frame, textvariable=self.t1_var, style="Value.TLabel").grid(row=1, column=1, padx=6, pady=6)
        ttk.Label(frame, textvariable=self.h1_var, style="Value.TLabel").grid(row=1, column=2, padx=6, pady=6)

        ttk.Label(frame, text="Sensor 2").grid(row=2, column=0, padx=6, pady=6, sticky="w")
        ttk.Label(frame, textvariable=self.t2_var, style="Value.TLabel").grid(row=2, column=1, padx=6, pady=6)
        ttk.Label(frame, textvariable=self.h2_var, style="Value.TLabel").grid(row=2, column=2, padx=6, pady=6)

        ttk.Separator(frame).grid(row=3, column=0, columnspan=3, sticky="ew", pady=(8, 4))

        ttk.Label(frame, text="Gjennomsnitt", font=("Segoe UI", 11, "bold")).grid(row=4, column=0, padx=6, pady=6, sticky="w")
        ttk.Label(frame, textvariable=self.ta_var, style="Value.TLabel").grid(row=4, column=1, padx=6, pady=6)
        ttk.Label(frame, textvariable=self.ha_var, style="Value.TLabel").grid(row=4, column=2, padx=6, pady=6)

        self.status_var = tk.StringVar(value="Starter sensorer…")
        ttk.Label(self, textvariable=self.status_var, style="Status.TLabel").pack(pady=(0, 8))

        self.reader = SensorReader()
        self.reader.start()

        self.poll_interval_ms = int(poll_interval_ms)
        self.after(self.poll_interval_ms, self._refresh)

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _refresh(self):
        data = self.reader.latest
        if data.get("error"):
            self.status_var.set(f"Feil: {data['error']}")
        else:
            self.status_var.set("Oppdatert")

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

p = Path("/mnt/data/gui_from_main_tk.py")
p.write_text(code, encoding="utf-8")
print(f"Wrote: {p}")
