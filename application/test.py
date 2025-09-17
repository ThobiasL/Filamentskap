from adapters.sensor_data_bridge_adapter import GuiReadingDataAdapter

values = GuiReadingDataAdapter().readData()

print(values)
