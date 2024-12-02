import unittest
from unittest.mock import patch, MagicMock
from app.config import get_secret

class TestConfig(unittest.TestCase):
    @patch("app.config.boto3.client")
    def test_get_secret(self, mock_boto_client):
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        mock_client.get_secret_value.return_value = {"SecretString": '{"key": "value"}'}

        secret = get_secret("test-secret", "us-east-1")
        self.assertEqual(secret, {"key": "value"})
