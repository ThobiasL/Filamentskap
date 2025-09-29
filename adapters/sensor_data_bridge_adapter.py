from typing import Sequence
from ports.DataBridge_port import guiDataBridge
from application.dataDokument import json_data_document

class guiReadingData_adapter(guiDataBridge):
    def __init__(self, temperature1=1, temperature2=1, average_temperature=1, humidity1=1, humidity2=1, average_humidity=1):
        self.temperature1 = temperature1
        self.temperature2 = temperature2
        self.average_temperature = average_temperature
        self.humidity1 = humidity1
        self.humidity2 = humidity2
        self.average_humidity = average_humidity
        self.document = json_data_document()

    def readData(self) -> list[float]:
        data = self.document.loadData()
        return data

    def sendData(self, data_inn: Sequence[float]) -> None:
        self.document.saveData(list(map(float, data_inn)))




'''
# adapters/sensor_data_bridge_adapter.py
from ports.DataBridge_port import gui_data_bridge
from application.data_bridge import read_latest

class GuiReadingDataAdapter(gui_data_bridge):
    def __init__(self) -> None:
        pass  # ingen manuelle verdier i ctor

    def readData(self) -> tuple[float, float, float, float, float, float]:
        r = read_latest()
        if not r:
            raise RuntimeError("Ingen data tilgjengelig ennå fra main.py")
        # Variant A: flat tuple (6 floats), i samme rekkefølge som du valgte
        return (r.temperature1, r.temperature2, r.average_temp,
                r.humidity1, r.humidity2, r.average_humidity)
'''
