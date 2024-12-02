import unittest
from unittest.mock import patch, MagicMock
from app.sensors import SensorReader

class TestSensorReader(unittest.TestCase):
    @patch("socket.socket")
    def test_read_sensors(self, mock_socket):
        mock_conn = MagicMock()
        mock_conn.recv.return_value = b'\x00\x00\xa0\x41\x00\x00\x70\x42\x00\x00\x48\x43'  # 20.0, 60.0, 200.0
        mock_socket.return_value.__enter__.return_value.accept.return_value = (mock_conn, None)

        reader = SensorReader()
        data = reader.read_sensors()
        self.assertEqual(data, {"temperature": 20.0, "humidity": 60.0, "sunlight": 200.0})
