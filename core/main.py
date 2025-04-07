import time
from adapters.BME280_adapter import BME280Sensor, average

def main():
    # Initialize adapters
    sensor1 = BME280Sensor(0x77)
    sensor2 = BME280Sensor(0x76)

    while True:
        try:
            # Les temperatur og fuktighet fra sensorene
            temperature1 = round(sensor1.read_temperature(),1)
            temperature2 = round(sensor2.read_temperature(),1)
            humidity1 = round(sensor1.read_humidity(),1)
            humidity2 = round(sensor2.read_humidity(),1)

            # Beregn gjennomsnittlig temperatur og fuktighet
            average_temp = round(average(temperature1, temperature2),1)
            average_humidity = round(average(humidity1, humidity2),1)

            # Skriv ut verdiene
            print(f"Sensor1 temperature: {temperature1} °C")
            print(f"Sensor2 Temperature: {temperature2} °C")
            print(f"Average Temperature: {average_temp} °C")

            print(f"Sensor1 humidity: {humidity1} %")
            print(f"Sensor2 humidity: {humidity2} %")
            print(f"Average Humidity: {average_humidity} %")

            time.sleep(2)

        except KeyboardInterrupt:
            print("Program terminated by user.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Lukker alle adaptere
            sensor1.close()
            sensor2.close()
            
if __name__ == "__main__":
    main()