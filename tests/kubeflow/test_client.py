import unittest
from unittest import mock

from krsh.kubeflow.pipeline import get_client


class TestClient(unittest.TestCase):
    @mock.patch("krsh.kubeflow.client.get_project_config")
    def test_get_client(self, mock_get_project_config):
        mock_get_project_config.return_value = {
            "host": "1.1.1.1",
            "namespaces": ["test-namespace"],
        }
        client = get_client("test-namespace")
        self.assertEqual(client.get_user_namespace(), "test-namespace")

        with self.assertRaises(ValueError):
            get_client("no_exists_ns")
