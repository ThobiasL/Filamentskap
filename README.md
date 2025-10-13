# Filamentskap

Traceback (most recent call last):
  File "/home/filamentskap/skap/Filamentskap/application/gui_bme280_tk.py", line 40, in _try_imports
    from BME280_adapter import BME280Sensor  # type: ignore
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'BME280_adapter'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/filamentskap/skap/Filamentskap/application/gui_bme280_tk.py", line 57, in <module>
    BME280Sensor, average = _try_imports()
                            ^^^^^^^^^^^^^^
  File "/home/filamentskap/skap/Filamentskap/application/gui_bme280_tk.py", line 51, in _try_imports
    raise ImportError(
ImportError: Kunne ikke importere BME280-adapteren og/eller average()-funksjonen. Sørg for at filene er tilgjengelige, og at 'bme280' og 'smbus2' er installert.
Original feil: No module named 'BME280_adapter'

