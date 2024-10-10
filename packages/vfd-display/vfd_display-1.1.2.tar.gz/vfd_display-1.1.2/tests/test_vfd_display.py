import unittest
from vfd_display import VfdDisplay
from unittest.mock import MagicMock

class TestVfdDisplay(unittest.TestCase):
    def setUp(self):
        self.vfd = VfdDisplay(enabled=False)  # Disable to avoid actual serial connection

    def test_write_line(self):
        self.vfd.ser = MagicMock()
        self.vfd.write_line("Test Message", line=1, column=1)
        self.vfd.ser.write.assert_called_with(b'Test Message')

    def test_clear_screen(self):
        self.vfd.ser = MagicMock()
        self.vfd.clear_screen()
        self.vfd.ser.write.assert_called_with(b'\x0C')

    def test_close(self):
        self.vfd.ser = MagicMock()
        self.vfd.close()
        self.vfd.ser.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
