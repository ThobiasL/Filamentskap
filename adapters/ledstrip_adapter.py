from ports.ledstrip_port import LedStripPort
import time
import board
import neopixel

class LEDStripAdapter(LedStripPort):
    def __init__(self, num_pixels: int, pin: int = board.D18, brightness: float = 1) -> None:
        self.num_pixels = num_pixels
        self.pin = pin
        self.brightness = brightness
        self.pixels = neopixel.NeoPixel(self.pin, self.num_pixels, brightness=self.brightness, auto_write=False)

    def set_color(self, color: tuple[int, int, int]) -> None:
        for i in range(self.num_pixels):
            self.pixels[i] = color
        self.pixels.show()

    def get_color(self) -> tuple[int, int, int]:
        return self.pixels[0]

    def clear(self) -> None:
        for i in range(self.num_pixels):
            self.pixels[i] = (0, 0, 0)
        self.pixels.show()
        time.sleep(0.1)
    
    def address_led(self,  start_address: int, end_address: int, set_color: tuple) -> None:
        for i in range(start_address, end_address):
            self.pixels[i] = set_color
        self.pixels.show()
        time.sleep(0.1)
