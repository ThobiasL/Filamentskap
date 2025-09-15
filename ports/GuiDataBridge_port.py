from abc import ABC, abstractmethod

class gui_data_bridge(ABC):
    @abstractmethod
    def update_temperature(self, temperature: float) -> None:
        pass

    @abstractmethod
    def update_humidity(self, humidity: float) -> None:
        pass

    @abstractmethod
    def update_average_temperature(self, average_temperature: float) -> None:
        pass

    @abstractmethod
    def update_average_humidity(self, average_humidity: float) -> None:
        pass