from ports.BME280_port import sensorPort, average
#import RPi.GPIO as gpio
import smbus2
import bme280

class BME280Sensor(sensorPort):
    def __init__(self, address, bus=1):
        self.address = address
        self.bus = smbus2.SMBus(bus)
        self.calibration_params = bme280.load_calibration_params(self.bus, self.address)

    def read_temperature(self) -> float:
        data = bme280.sample(self.bus, self.address, self.calibration_params)
        return data.temperature

    def read_humidity(self) -> float:
        data = bme280.sample(self.bus, self.address, self.calibration_params)
        return data.humidity