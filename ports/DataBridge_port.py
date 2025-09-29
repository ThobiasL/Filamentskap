from abc import ABC, abstractmethod

class guiDataBridge(ABC):
    @abstractmethod
    def readData(self) -> list[float]:
        pass

    @abstractmethod
    def sendData(self, data_inn) -> list[float]:
        pass