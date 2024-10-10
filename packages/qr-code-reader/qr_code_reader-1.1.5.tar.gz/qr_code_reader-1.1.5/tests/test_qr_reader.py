import unittest
from QRCodeReader import QRCodeReader
import queue

class TestQRCodeReader(unittest.TestCase):
    def test_qr_reader(self):
        q = queue.Queue()
        qr_reader = QRCodeReader(q)
        self.assertEqual(qr_reader.Read(), None)

if __name__ == '__main__':
    unittest.main()

