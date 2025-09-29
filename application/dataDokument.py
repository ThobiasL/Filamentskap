import json
from typing import Sequence

class json_data_document:
    def __init__(self, filename='../out/SensorData.json'):
        self.filename = filename

    def saveData(self, data: Sequence[float]) -> None:
        t1, t2, at, h1, h2, ah = map(float, data)
        data_list = (t1, t2, at, h1, h2, ah)
        with open(self.filename, 'w') as f:
            json.dump(data_list, f)

    def loadData(self) -> list[float]:
        with open(self.filename, 'r') as f:
            data_dict = json.load(f)
        return data_dict