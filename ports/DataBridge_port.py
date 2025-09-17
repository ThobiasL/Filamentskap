from abc import ABC, abstractmethod

class gui_data_bridge(ABC):
    @abstractmethod
    def readData(self) -> tuple[float, float, float, float, float, float]:
        pass

    @abstractmethod
    def updateData(self, data: tuple[float, float, float, float, float, float]) -> None:
        pass