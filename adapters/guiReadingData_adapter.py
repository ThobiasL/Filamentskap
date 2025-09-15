from ports.GuiDataBridge_port import gui_data_bridge

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
