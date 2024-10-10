import unittest
import queue
from qr_code_reader import QRCodeReader
from unittest.mock import patch, MagicMock


class TestQRCodeReader(unittest.TestCase):

    def setUp(self):
        """Set up a queue and QRCodeReader instance before each test."""
        self.q = queue.Queue()
        self.reader = QRCodeReader(self.q)

    def test_read_qr_code(self):
        """Test that a QR code is read correctly."""
        input_data = "123456"
        # Simulate input by using a patch on input()
        with patch('builtins.input', return_value=input_data):
            result = self.reader.Read()
            self.assertEqual(result, input_data)

    def test_empty_queue(self):
        """Test that the reader returns None when the queue is empty."""
        result = self.reader.Read()
        self.assertIsNone(result)

    def test_keyboard_interrupt(self):
        """Test handling of KeyboardInterrupt."""
        with patch('builtins.input', side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                self.reader.Read()

    def test_eof_error(self):
        """Test handling of EOFError."""
        with patch('builtins.input', side_effect=EOFError):
            result = self.reader.Read()
            self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()

