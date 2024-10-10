# Relay Controller

A relay controller module for Python.

## Installation

```bash
pip install relay-controller
```
## Usage
```bash
from relay_controller.controller import RController

relay_controller = RController("/dev/ttyUSB0", 1)  # Example usage
relay_controller.activate_relay(duration=5)  # Activate for 5 seconds
```

