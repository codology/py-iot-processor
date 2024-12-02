import unittest
from unittest.mock import patch, MagicMock
from app.metrics import MetricsCollector

class TestMetricsCollector(unittest.TestCase):
    @patch("app.metrics.boto3.client")
    def test_publish_metric(self, mock_boto_client):
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client

        metrics_collector = MetricsCollector()
        metrics_collector.publish_metric("Temperature", 25.5)

        mock_client.put_metric_data.assert_called_once_with(
            Namespace="IoTData",
            MetricData=[{"MetricName": "Temperature", "Value": 25.5, "Unit": "None"}]
        )
