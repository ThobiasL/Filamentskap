from core.main import average

class guiReadingData_adapter:
    def __init__(self, sensor1, sensor2):
        self.sensor1 = sensor1
        self.sensor2 = sensor2

    def readData(self):
        temperature1 = round(self.sensor1.read_temperature(),1)
        temperature2 = round(self.sensor2.read_temperature(),1)
        humidity1 = round(self.sensor1.read_humidity(),1)
        humidity2 = round(self.sensor2.read_humidity(),1)

        average_temperature = average(temperature1, temperature2)
        average_humidity = average(humidity1, humidity2)

        return temperature1, temperature2, humidity1, humidity2, average_temperature, average_humidity