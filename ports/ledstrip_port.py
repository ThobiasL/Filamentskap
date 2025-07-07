from abc import ABC, abstractmethod

class LedStripPort(ABC):
    @abstractmethod
    def set_color(self, color: tuple[int, int, int]) -> None:
        """Set the color of the LED strip.

        Args:
            color (tuple[int, int, int]): A tuple representing the RGB color.
        """
        pass

    @abstractmethod
    def get_color(self) -> tuple[int, int, int]:
        """Get the current color of the LED strip.

        Returns:
            tuple[int, int, int]: A tuple representing the RGB color.
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear the LED strip."""
        pass

    @abstractmethod
    def address_led(self, start_address: int, end_address: int, set_color: tuple) -> None:
        """Set the address of the LED strip.

        Args:
            address (int): The address of the LED strip.
        """
        pass