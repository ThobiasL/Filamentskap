import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Add the parent directory to the Python path
from adapters.BME280_adapter import BME280Sensor, average
from adapters.ledstrip_adapter import LEDStripAdapter
import time

def main():
    # Seting up variables
    normal_led_state = (255, 255, 255)
    warning_led_state = (255, 0, 0) # Red color for warning
    humidity_limit = 60
    led_warning_signal = False
    timer = 0
    timer_limit = 20
    maneul_override = False

    # Initialize adapters for BME280 sensors
    sensor1 = BME280Sensor(0x77)
    sensor2 = BME280Sensor(0x76)

    # Initialize adapters for LED strip
    ledstrip = LEDStripAdapter(17, pin = 18) # GPIO 18
    ledstrip.clear()
    ledstrip.set_color(normal_led_state)
    time.sleep(0.1)

    # Function for LED strip
    def warning_led(average_humidity):
        if not maneul_override:
            if average_humidity > humidity_limit and not led_warning_signal:
                ledstrip.clear()
                ledstrip.set_color(warning_led_state)
                led_warning_signal = True
            
            elif average_humidity < humidity_limit and led_warning_signal:
                if timer > timer_limit:
                    ledstrip.clear()
                    ledstrip.set_color(normal_led_state)
                    led_warning_signal = False
                    timer = 0
                else:
                    timer += 1
                    ledstrip.clear()
                    ledstrip.set_color(warning_led_state)
        elif maneul_override and timer > timer_limit:
            maneul_override = False
            timer = 0
        else:
            timer += 1

        
        time.sleep(0.1)

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

            # Sjekk om fuktigheten er for høy
            '''warning_led(average_humidity)'''

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