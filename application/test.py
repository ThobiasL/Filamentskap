from adapters.sensor_data_bridge_adapter import guiReadingData_adapter

measurement = guiReadingData_adapter()
liste = [22.5, 23.0, 22.75, 55.0, 57.0, 56.0]
measurement.sendData(liste)
values = measurement.readData()

print(values)
print(values[0])
print(values[1])
print(values[2])
