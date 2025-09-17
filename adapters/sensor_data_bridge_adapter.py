from ports.DataBridge_port import gui_data_bridge

class guiReadingData_adapter(gui_data_bridge):
    def __init__(self, temperature1, temperature2, average_temperature, humidity1, humidity2, average_humidity):
        self.temperature1 = temperature1
        self.temperature2 = temperature2
        self.average_temperature = average_temperature
        self.humidity1 = humidity1
        self.humidity2 = humidity2
        self.average_humidity = average_humidity

    def readData(self) -> tuple[float, float, float, float, float, float]:
        return (self.temperature1, self.temperature2, self.average_temperature, self.humidity1, self.humidity2, self.average_humidity)


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
