import RPi.GPIO as gpio
import time
import smbus2
import bme280

address_1 = 0x77
address_2 = 0x76

bus = smbus2.SMBus(1)

calibration_params = bme280.load_calibration_params(bus, address_1)
calibration_params = bme280.load_calibration_params(bus, address_2)

def average(variabel1, variabel2):
    return (variabel1 + variabel2)/2

while True:
    try:
        data_1 = bme280.sample(bus, address_1, calibration_params)
        data_2 = bme280.sample(bus, address_2, calibration_params)

        temperature_1 = data_1.temperature
        temperature_2 = data_2.temperature
        print(f"temperature 1: {round(temperature_1,1)}")
        print(f"temperature 2: {round(temperature_2,1)}")
        print(f"average temp: {round(average(temperature_1, temperature_2),1)}")

        humidity_1 = data_1.humidity
        humidity_2 = data_2.humidity
        print(f"humidity 1: {round(humidity_1,1)}%")
        print(f"humidity 2: {round(humidity_2,1)}%")
        print(f"average humidity: {round(average(humidity_1, humidity_2),1)}%")

        time.sleep(2)

    except Exception as e:
        print("Error: ", str(e))