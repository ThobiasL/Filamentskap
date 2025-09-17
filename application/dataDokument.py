'''
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


data = guiReadingData_adapter().readData()
json_data = json.dumps(data)
print(json_data)

with open('/tmp/env_readings.json', 'w') as f:
    f.write(json_data)
'''

from adapters.sensor_data_bridge_adapter import guiReadingData_adapter
import json

class json_data_document:
    def __init__(self, filename='../application/SensorData.json'):
        self.filename = filename

    def save(self, data: tuple[float, float, float, float, float, float]) -> None:
        data_dict = {
            "temperature1": data[0],
            "temperature2": data[1],
            "average_temperature": data[2],
            "humidity1": data[3],
            "humidity2": data[4],
            "average_humidity": data[5]
        }
        with open(self.filename, 'w') as f:
            json.dump(data_dict, f)

    def load(self) -> tuple[float, float, float, float, float, float]:
        data = guiReadingData_adapter().readData()
        open with open(self.filename, 'r') as f:
            data_dict = json.load(f)
        return (
            data_dict.get("temperature1", data[0]),
            data_dict.get("temperature2", data[1]),
            data_dict.get("average_temperature", data[2]),
            data_dict.get("humidity1", data[3]),
            data_dict.get("humidity2", data[4]),
            data_dict.get("average_humidity", data[5])
        )