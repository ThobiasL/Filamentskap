from abc import ABC, abstractmethod

class SensorPort(ABC):
    @abstractmethod
    def read_temperature(self) -> float:
        pass

    @abstractmethod
    def read_humidity(self) -> float:
        pass

def average(value1: float, value2: float) -> float:
    return (value1 + value2) / 2