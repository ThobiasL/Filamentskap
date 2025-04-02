# Filamentskap

test
Can't open /dev/mem: Permission denied
Traceback (most recent call last):
  File "/home/filamentskap/skap/Filamentskap/core/main.py", line 91, in <module>
    main()
  File "/home/filamentskap/skap/Filamentskap/core/main.py", line 24, in main
    ledstrip.clear()
  File "/home/filamentskap/skap/Filamentskap/adapters/ledstrip_adapter.py", line 24, in clear
    self.pixels.show()
  File "/home/filamentskap/skap/skap/lib/python3.11/site-packages/adafruit_pixelbuf.py", line 204, in show
    return self._transmit(self._post_brightness_buffer)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/filamentskap/skap/skap/lib/python3.11/site-packages/neopixel.py", line 181, in _transmit
    neopixel_write(self.pin, buffer)
  File "/home/filamentskap/skap/skap/lib/python3.11/site-packages/neopixel_write.py", line 49, in neopixel_write
    return _neopixel.neopixel_write(gpio, buf)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/filamentskap/skap/skap/lib/python3.11/site-packages/adafruit_blinka/microcontroller/bcm283x/neopixel.py", line 78, in neopixel_write
    raise RuntimeError(
RuntimeError: NeoPixel support requires running with sudo, please try again!
swig/python detected a memory leak of type 'ws2811_t *', no destructor found.

