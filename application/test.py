from adapters.sensor_data_bridge_adapter import guiReadingData_adapter

measurement = guiReadingData_adapter()
values = measurement.readData()

print(values)