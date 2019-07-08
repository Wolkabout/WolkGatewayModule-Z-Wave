import wolk_gateway_module as wolk


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

dimmer_template = wolk.ActuatorTemplate(
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
    actuators=[dimmer_template],
)

smart_dimmer_device = wolk.Device(
    "Smart Dimmer", "dimmer", smart_dimmer_template
)
