# WolkGatewayModule-Z-Wave
WolkGateway module for connecting Z-Wave devices to WolkAbout IoT Platform by communicating with [WolkGateway](https://github.com/Wolkabout/WolkGateway).


## Requirements

* Python 3.7

## Dependencies

This project was built using [PyZwaver](https://github.com/robertmuth/PyZwaver) that handles all Z-Wave communication and [WolkGatewayModule-SDK-Python](https://github.com/Wolkabout/WolkGatewayModule-SDK-Python) that manages the connection to WolkGateway.

They can be installed by running:

```console
sudo ./setup.sh
```

## Usage

Edit **configuration.json** with the `serial_port` where the primary controller is connected,
and setup the `host` and `port` to refer to the WolkGateway's MQTT broker.
`module_name` is used to uniquely identify a module on WolkGateway.

```javascript
{
  "serial_port": "/dev/ttyACM0", // Primary Z-Wave controller
  "host": "localhost",           // Host address of WolkGateway
  "port": 1883,                  // Port of WolkGateway's MQTT broker
  "module_name": "Z-Wave Module" // Unique module identifier
}
```

Managing the communication with Z-Wave nodes can be seen in `demo.py` that uses [Aeotec Z-Stick](https://aeotec.com/z-wave-usb-stick) controller and [Aeotec Smart Dimmer 6](https://aeotec.com/z-wave-plug-in-dimmer).
The example gets the current energy consumption periodically from the smart plug and accepts commands from WolkAbout IoT Platform to change the current value of the dimmer.