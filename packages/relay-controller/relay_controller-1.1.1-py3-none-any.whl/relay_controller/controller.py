import os
from time import sleep
import logging

# Custom logging setup for colored output
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'INFO': '\033[92m',  # Green
        'ERROR': '\033[91m',  # Red
        'WARNING': '\033[93m',  # Yellow/Orange
        'RESET': '\033[0m'  # Reset color
    }

    def format(self, record):
        level_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        message = super().format(record)
        return f"{level_color}{message}{self.COLORS['RESET']}"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
for handler in logging.root.handlers:
    handler.setFormatter(ColoredFormatter())

try:
    import pyhid_usb_relay
except ModuleNotFoundError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip3", "install", "pyhid-usb-relay"])
    import pyhid_usb_relay

class RController:
    """Class responsible for controlling the relay."""

    def __init__(self, relay, Relay_Number):
        self.Relay_Number = Relay_Number
        self.relay = None
        try:
            self.relay = pyhid_usb_relay.find()
        except Exception as e:
            logging.error("Relay not found: %s", e)

    def activate_relay(self, duration=1):
        """Activates the relay for a certain duration."""
        if self.relay is None:
            logging.error("Relay not initialized")
            return

        try:
            logging.info("Relay activated.")
            self.relay.set_state(self.Relay_Number, 1)  # Turn On
            sleep(duration)
            self.relay.set_state(self.Relay_Number, 0)  # Turn Off
        except Exception as e:
            logging.error("Failed to control relay: %s", e)

    def cleanup(self):
        """Cleans up the GPIO on exit."""
        pass
