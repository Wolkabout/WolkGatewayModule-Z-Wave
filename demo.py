import json
import time

import wolk_gateway_module as wolk

import zwave
import devices
import handlers

# # uncomment to enable debug
# wolk.logging_config("debug")


try:
    with open("configuration.json", encoding="utf-8") as file:
        configuration = json.load(file)
except Exception as e:
    print(f"Failed to open configuration file: {e}")
    quit()

wolk_module = wolk.Wolk(
    configuration["host"],
    configuration["port"],
    configuration["module_name"],
    handlers.node_status_provider,
    actuation_handler=handlers.handle_actuation,
    acutator_status_provider=handlers.get_actuator_status,
)
wolk_module.add_device(devices.smart_dimmer_device)

wolk_module.connect()
wolk_module.publish()

time.sleep(5)  # Allow connect method to ping nodes for their status

wolk_module.publish_acutator_status("smart_dimmer6", "D")

try:
    while True:
        for n in zwave.controller.nodes:
            node = zwave.nodeset.GetNode(n)
            if node.IsInterviewed():
                if node not in zwave.controller.failed_nodes:
                    node.RefreshDynamicValues()
            time.sleep(1)

        node_number = 2
        node = zwave.nodeset.GetNode(node_number)

        if not node.IsInterviewed():
            wolk_module.publish_device_status(
                "smart_dimmer6", wolk.DeviceStatus.OFFLINE
            )
            continue

        for value in node.values.Meters():

            if value[2] == "kWh":
                wolk_module.add_sensor_reading(
                    "smart_dimmer6",
                    "EC",
                    value[3],
                    int(round(time.time() * 1000)),
                )
            elif value[2] == "W":
                wolk_module.add_sensor_reading(
                    "smart_dimmer6",
                    "P",
                    value[3],
                    int(round(time.time() * 1000)),
                )
            elif value[2] == "V":
                wolk_module.add_sensor_reading(
                    "smart_dimmer6",
                    "V",
                    value[3],
                    int(round(time.time() * 1000)),
                )
            elif value[2] == "A":
                wolk_module.add_sensor_reading(
                    "smart_dimmer6",
                    "I",
                    value[3],
                    int(round(time.time() * 1000)),
                )

        wolk_module.publish()
        time.sleep(5)

except Exception as e:
    print(f"Exception occurred: {e}")
    zwave.driver.Terminate()
    wolk_module.disconnect()
    quit()
