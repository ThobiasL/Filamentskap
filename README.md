# Filamentskap

test
Traceback (most recent call last):
  File "/home/filamentskap/skap/Filamentskap/core/main.py", line 91, in <module>
    main()
  File "/home/filamentskap/skap/Filamentskap/core/main.py", line 23, in main
    ledstrip = LEDStripAdapter(17, pin = 18)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/filamentskap/skap/Filamentskap/adapters/ledstrip_adapter.py", line 11, in __init__
    self.pixels = neopixel.NeoPixel(self.pin, self.num_pixels, brightness=self.brightness, auto_write=False)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/filamentskap/skap/skap/lib/python3.11/site-packages/neopixel.py", line 142, in __init__
    self.pin = digitalio.DigitalInOut(pin)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/filamentskap/skap/skap/lib/python3.11/site-packages/digitalio.py", line 192, in __init__
    self._pin = Pin(pin.id)
                    ^^^^^^
AttributeError: 'int' object has no attribute 'id'
