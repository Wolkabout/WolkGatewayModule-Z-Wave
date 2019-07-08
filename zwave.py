import json

import pyzwaver


try:
    with open("configuration.json", encoding="utf-8") as file:
        configuration = json.load(file)
except Exception as e:
    print(f"Failed to open configuration file: {e}")
    quit()

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
