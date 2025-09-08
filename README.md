# Filamentskap

Traceback (most recent call last):
  File "/home/filamentskap/skap/Filamentskap/core/main.py", line 93, in <module>
    main()
  File "/home/filamentskap/skap/Filamentskap/core/main.py", line 19, in main
    sensor1 = BME280Sensor(0x77)
              ^^^^^^^^^^^^^^^^^^
  File "/home/filamentskap/skap/Filamentskap/adapters/BME280_adapter.py", line 9, in __init__
    self.calibration_params = bme280.load_calibration_params(self.bus, self.address)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/filamentskap/skap/skap/lib/python3.11/site-packages/bme280/__init__.py", line 156, in load_calibration_params
    compensation_params.dig_T3 = read.signed_short(0x8C)
                                 ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/filamentskap/skap/skap/lib/python3.11/site-packages/bme280/reader.py", line 43, in signed_short
    word = self.unsigned_short(register)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/filamentskap/skap/skap/lib/python3.11/site-packages/bme280/reader.py", line 40, in unsigned_short
    return self._bus.read_word_data(self._address, register) & 0xffff
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/filamentskap/skap/skap/lib/python3.11/site-packages/smbus2/smbus2.py", line 476, in read_word_data
    ioctl(self.fd, I2C_SMBUS, msg)
OSError: [Errno 5] Input/output error
(skap) root@raspberrypi:/home/filamentskap/skap/Filamentskap/core# python main.py
Traceback (most recent call last):
  File "/home/filamentskap/skap/Filamentskap/core/main.py", line 93, in <module>
    main()
  File "/home/filamentskap/skap/Filamentskap/core/main.py", line 19, in main
    sensor1 = BME280Sensor(0x77)
              ^^^^^^^^^^^^^^^^^^
  File "/home/filamentskap/skap/Filamentskap/adapters/BME280_adapter.py", line 9, in __init__
    self.calibration_params = bme280.load_calibration_params(self.bus, self.address)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/filamentskap/skap/skap/lib/python3.11/site-packages/bme280/__init__.py", line 156, in load_calibration_params
    compensation_params.dig_T3 = read.signed_short(0x8C)
                                 ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/filamentskap/skap/skap/lib/python3.11/site-packages/bme280/reader.py", line 43, in signed_short
    word = self.unsigned_short(register)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/filamentskap/skap/skap/lib/python3.11/site-packages/bme280/reader.py", line 40, in unsigned_short
    return self._bus.read_word_data(self._address, register) & 0xffff
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/filamentskap/skap/skap/lib/python3.11/site-packages/smbus2/smbus2.py", line 476, in read_word_data
    ioctl(self.fd, I2C_SMBUS, msg)
OSError: [Errno 5] Input/output error


