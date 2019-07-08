import time

import pyzwaver
import wolk_gateway_module as wolk

import zwave


def node_status_provider(device_key):
    """Ping network node to get current state."""
    nodes = zwave.controller.nodes.copy()
    nodes.remove(zwave.controller.GetNodeId())
    if device_key == "dimmer":
        node_number = 2
        zwave.translator.Ping(node_number, 5, False, "status_request")
        time.sleep(1.5)
        node = zwave.nodeset.GetNode(node_number)
        if node.IsInterviewed():
            if node in zwave.controller.failed_nodes:
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
            node = zwave.nodeset.GetNode(node_number)
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
            node = zwave.nodeset.GetNode(node_number)
            if (
                not node.IsInterviewed()
                or node in zwave.controller.failed_nodes
            ):
                return wolk.ActuatorState.ERROR, None
            node.RefreshDynamicValues()
            time.sleep(0.5)
            for value in sorted(node.values.Values()):
                if value[1] == "SwitchMultilevel_Report":
                    return wolk.ActuatorState.READY, value[2]["level"]
