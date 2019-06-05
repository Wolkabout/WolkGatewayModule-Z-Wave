import json
import time

import pyzwaver
import wolk_gateway_module as wolk

# # uncomment to enable debug
# wolk.logging_config("debug")


try:
    with open("configuration.json", encoding="utf-8") as file:
        configuration = json.load(file)
except Exception as e:
    print(f"Failed to open configuration file: {e}")
    quit()

# Z-Wave setup
serial_device = pyzwaver.driver.MakeSerialDevice(configuration["serial_port"])
driver = pyzwaver.driver.Driver(serial_device)
controller = pyzwaver.controller.Controller(driver)
controller.Initialize()
controller.WaitUntilInitialized()
controller.UpdateRoutingInfo()
translator = pyzwaver.command_translator.CommandTranslator(driver)
nodeset = pyzwaver.node.Nodeset(translator, controller.GetNodeId())


class TestListener:
    """
    Demonstrates how to hook into the stream of messages
    sent to the controller from other nodes
    """

    def __init__(self):
        pass

    def put(self, n, ts, key, values):
        name = "@NONE@"
        if key[0] is not None:
            name = pyzwaver.command.StringifyCommand(key)
        print(f"RECEIVED [{n}]: {name} - {values}")


translator.AddListener(TestListener())


# Wolk Device setup for Aeotec Smart Dimmer 6

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


def node_status_provider(device_key):
    """Ping network node to get current state."""
    nodes = controller.nodes.copy()
    nodes.remove(controller.GetNodeId())
    if device_key == "dimmer":
        node_number = 2
        translator.Ping(node_number, 5, False, "status_request")
        time.sleep(1.5)
        node = nodeset.GetNode(node_number)
        if node.IsInterviewed():
            if node in controller.failed_nodes:
                return wolk.DeviceStatus.OFFLINE
            return wolk.DeviceStatus.CONNECTED
        else:
            return wolk.DeviceStatus.OFFLINE


def handle_actuation(device_key, reference, value):
    """
    Set device actuator identified by reference to value.
    """
    if device_key == "dimmer":
        if reference == "D":
            node_number = 2
            node = nodeset.GetNode(node_number)
            node.BatchCommandSubmitFilteredFast(
                pyzwaver.command_helper.MultilevelSwitchSet(value)
            )


def get_actuator_status(device_key, reference):
    """
    Get current actuator status identified by device key and reference.
    """
    if device_key == "dimmer":
        if reference == "D":
            node_number = 2
            node = nodeset.GetNode(node_number)
            if not node.IsInterviewed() or node in controller.failed_nodes:
                return wolk.ActuatorState.ERROR, None
            node.RefreshDynamicValues()
            time.sleep(0.5)
            for value in sorted(node.values.Values()):
                if value[1] == "SwitchMultilevel_Report":
                    return wolk.ActuatorState.READY, value[2]["level"]


wolk_module = wolk.Wolk(
    configuration["host"],
    configuration["port"],
    configuration["module_name"],
    node_status_provider,
    actuation_handler=handle_actuation,
    acutator_status_provider=get_actuator_status,
)
wolk_module.add_device(smart_dimmer_device)

wolk_module.connect()

wolk_module.publish()

wolk_module.publish_acutator_status("dimmer", "D")

time.sleep(5)

try:
    while True:
        for n in controller.nodes:
            node = nodeset.GetNode(n)
            if node.IsInterviewed():
                if node not in controller.failed_nodes:
                    node.RefreshDynamicValues()
            time.sleep(1)

        node_number = 2
        node = nodeset.GetNode(node_number)

        if not node.IsInterviewed():
            wolk_module.publish_device_status("dimmer")
            continue

        for value in node.values.Meters():

            if value[2] == "kWh":
                wolk_module.add_sensor_reading(
                    "dimmer", "EC", value[3], int(round(time.time() * 1000))
                )
            elif value[2] == "W":
                wolk_module.add_sensor_reading(
                    "dimmer", "P", value[3], int(round(time.time() * 1000))
                )
            elif value[2] == "V":
                wolk_module.add_sensor_reading(
                    "dimmer", "V", value[3], int(round(time.time() * 1000))
                )
            elif value[2] == "A":
                wolk_module.add_sensor_reading(
                    "dimmer", "I", value[3], int(round(time.time() * 1000))
                )

        wolk_module.publish()
        time.sleep(5)

except Exception as e:
    print(f"Exception occurred: {e}")
    driver.Terminate()
    wolk_module.disconnect()
    quit()
