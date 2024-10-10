import unittest
import queue
from qr_code_reader import QRCodeReader


class TestQRCodeReader(unittest.TestCase):

    def setUp(self):
        self.q = queue.Queue()
        self.reader = QRCodeReader(self.q)

    def test_read_qr_code(self):
        # Simulate input
        input_data = "123456"
        self.q.put(input_data)  # Simulate that the queue has an item
        result = self.reader.Read()
        self.assertEqual(result, input_data)

    def test_empty_queue(self):
        result = self.reader.Read()
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()

