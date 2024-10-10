import unittest
from unittest.mock import MagicMock, patch
from relay_controller.controller import RController

class TestRController(unittest.TestCase):

    @patch('relay_controller.controller.pyhid_usb_relay.find')
    def setUp(self, mock_find):
        # Mock the relay hardware
        self.mock_relay = MagicMock()
        mock_find.return_value = self.mock_relay
        self.relay_controller = RController("/dev/ttyUSB0", 1)

    def test_relay_initialization(self):
        """Test that the relay controller initializes correctly."""
        self.assertIsNotNone(self.relay_controller.relay)
        self.assertEqual(self.relay_controller.Relay_Number, 1)

    def test_activate_relay(self):
        """Test that the relay gets activated and deactivated."""
        self.relay_controller.activate_relay(duration=2)
        self.mock_relay.set_state.assert_any_call(1, 1)  # Relay on
        self.mock_relay.set_state.assert_any_call(1, 0)  # Relay off

    def test_activate_relay_with_no_relay(self):
        """Test that activation fails when relay is not initialized."""
        self.relay_controller.relay = None
        with self.assertLogs(level='ERROR') as cm:
            self.relay_controller.activate_relay()
        self.assertIn('Relay not initialized', cm.output[0])

    def test_relay_not_found(self):
        """Test handling when the relay is not found."""
        with patch('relay_controller.controller.pyhid_usb_relay.find', side_effect=Exception("Relay not found")):
            relay_controller = RController("/dev/ttyUSB0", 1)
            with self.assertLogs(level='ERROR') as cm:
                relay_controller.activate_relay()
            self.assertIn("Relay not found", cm.output[0])

if __name__ == '__main__':
    unittest.main()
