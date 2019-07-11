import wolk_gateway_module as wolk


# Aeotec Smart Dimmer 6

power_sensor = wolk.SensorTemplate(
    name="Power",
    reference="P",
    reading_type_name=wolk.ReadingTypeName.POWER,
    unit=wolk.ReadingTypeMeasurementUnit.WATT,
)

voltage_sensor = wolk.SensorTemplate(
    name="Voltage",
    reference="V",
    reading_type_name=wolk.ReadingTypeName.BATTERY_VOLTAGE,
    unit=wolk.ReadingTypeMeasurementUnit.VOLT,
)

current_sensor = wolk.SensorTemplate(
    name="Electric Current",
    reference="I",
    reading_type_name=wolk.ReadingTypeName.ELECTRIC_CURRENT,
    unit=wolk.ReadingTypeMeasurementUnit.AMPERE,
    minimum=0,
    maximum=100,
)

power_consumption_sensor = wolk.SensorTemplate(
    name="Energy consumption",
    reference="EC",
    reading_type_name=wolk.ReadingTypeName.BATTERY_POWER,
    unit=wolk.ReadingTypeMeasurementUnit.BATTERY_X1000,
    minimum=0,
    maximum=100,
)

dimmer_actuator = wolk.ActuatorTemplate(
    name="Dimmer",
    reference="D",
    data_type=wolk.DataType.NUMERIC,
    minimum=0,
    maximum=100,
)

smart_dimmer_template = wolk.DeviceTemplate(
    sensors=[
        power_sensor,
        voltage_sensor,
        current_sensor,
        power_consumption_sensor,
    ],
    actuators=[dimmer_actuator],
)

smart_dimmer_device = wolk.Device(
    "Smart Dimmer", "smart_dimmer6", smart_dimmer_template
)

# Aeotec LED Bulb 6

LED_dimmer_template = wolk.ActuatorTemplate(
    name="Dimmer",
    reference="D",
    data_type=wolk.DataType.NUMERIC,
    minimum=0,
    maximum=100,
)

LED_bulb_template = wolk.DeviceTemplate(actuators=[LED_dimmer_template])

LED_bulb_device = wolk.Device("LED Bulb", "LED_Bulb6", LED_bulb_template)


# Aeotec Multi Sensor 6

illuminance_sensor = wolk.SensorTemplate(
    name="Illuminance",
    reference="IL",
    reading_type_name=wolk.ReadingTypeName.ILLUMINANCE,
    unit=wolk.ReadingTypeMeasurementUnit.LUX,
    minimum=0,
    maximum=30000,
)

humidity_sensor = wolk.SensorTemplate(
    name="Humidity",
    reference="H",
    reading_type_name=wolk.ReadingTypeName.HUMIDITY,
    unit=wolk.ReadingTypeMeasurementUnit.PERCENT,
    minimum=0,
    maximum=100,
)

temperature_sensor = wolk.SensorTemplate(
    name="Temperature",
    reference="T",
    reading_type_name=wolk.ReadingTypeName.TEMPERATURE,
    unit=wolk.ReadingTypeMeasurementUnit.CELSIUS,
    minimum=-10,
    maximum=50,
)

ultraviolet_sensor = wolk.SensorTemplate(
    name="Ultraviolet",
    reference="UV",
    data_type=wolk.DataType.NUMERIC,
    minimum=0,
    maximum=10,
)


multi_sensor_template = wolk.DeviceTemplate(
    sensors=[
        illuminance_sensor,
        humidity_sensor,
        temperature_sensor,
        ultraviolet_sensor,
    ]
)

multi_sensor_device = wolk.Device(
    "MultiSensor 6", "multi_sensor6", multi_sensor_template
)
