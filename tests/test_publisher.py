import unittest
from unittest.mock import patch, MagicMock
from app.publisher import publish_data

class TestPublisher(unittest.TestCase):
    @patch("app.publisher.SensorReader.read_sensors")
    @patch("app.publisher.get_secret")
    @patch("app.publisher.boto3.client")
    def test_publish_data(self, mock_boto_client, mock_get_secret, mock_read_sensors):
        mock_get_secret.return_value = {"key": "value"}
        mock_kinesis_client = MagicMock()
        mock_boto_client.return_value = mock_kinesis_client
        mock_read_sensors.return_value = {"temperature": 20.0, "humidity": 50.0, "sunlight": 300.0}

        mock_kinesis_client.put_record.return_value = None  # Mock Kinesis put_record
        mock_metrics_client = MagicMock()
        with patch("app.publisher.MetricsCollector", return_value=mock_metrics_client):
            publish_data("test-stream", "us-east-1", "test-secret")
        
        mock_kinesis_client.put_record.assert_called_once()
        mock_metrics_client.publish_metric.assert_called()
