# data_bridge.py
from __future__ import annotations
import json, os, tempfile, time
from dataclasses import dataclass, asdict
from typing import Optional

_DATA_FILE = "/tmp/env_readings.json"

@dataclass
class Readings:
    temperature1: float
    temperature2: float
    average_temp: float
    humidity1: float
    humidity2: float
    average_humidity: float

def _atomic_write(path: str, text: str) -> None:
    d = os.path.dirname(path) or "."
    fd, tmp = tempfile.mkstemp(prefix=".tmp_readings_", dir=d)
    try:
        with os.fdopen(fd, "w") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)  # atomisk
    finally:
        try:
            if os.path.exists(tmp):
                os.remove(tmp)
        except OSError:
            pass

def update_readings(r: Readings) -> None:
    _atomic_write(_DATA_FILE, json.dumps(asdict(r), separators=(",", ":")))

def read_latest() -> Optional[Readings]:
    try:
        with open(_DATA_FILE) as f:
            obj = json.load(f)
        return Readings(**obj)
    except Exception:
        return None
'''
from adapters.guiReadingData_adapter import GuiReadingDataAdapter
import json

data = GuiReadingDataAdapter().readData()
json_data = json.dumps(data)
print(json_data)

with open('/tmp/env_readings.json', 'w') as f:
    f.write(json_data)
'''