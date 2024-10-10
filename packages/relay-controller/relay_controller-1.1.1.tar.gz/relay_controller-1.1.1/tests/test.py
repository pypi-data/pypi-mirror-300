from relay_controller.controller import RController

relay_controller = RController("/dev/ttyUSB0", 1)
relay_controller.activate_relay()
