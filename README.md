# Filamentskap

test
sys.path
/home/filamentskap/skap/Filamentskap/core
/usr/lib/python311.zip
/usr/lib/python3.11
/usr/lib/python3.11/lib-dynload
/home/filamentskap/skap/skap/lib/python3.11/site-packages
/home/filamentskap/skap/Filamentskap
Traceback (most recent call last):
  File "/home/filamentskap/skap/Filamentskap/core/main.py", line 7, in <module>
    from adapters.BME280_adapter import BME280Sensor, average
  File "/home/filamentskap/skap/Filamentskap/adapters/BME280_adapter.py", line 1, in <module>
    from ports.BME280_port import sensorPort, average
ImportError: cannot import name 'sensorPort' from 'ports.BME280_port' (/home/filamentskap/skap/Filamentskap/ports/BME280_port.py)
