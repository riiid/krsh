import os
import shutil
import tempfile
import unittest
from unittest import mock

import yaml

from krsh.cmd.cmd_configure import cmd_configure


class TestCommandConfigure(unittest.TestCase):
    def setUp(self):
        self.sample_path = os.path.join(os.path.dirname(__file__), "../samples")

    @mock.patch("krsh.cmd.cmd_configure.click.prompt")
    def test_cmd_configure_when_configured(self, mock_icon_prompt):
        mock_icon_prompt.side_effect = ["0.0.0.0", "test-ns"]
        with tempfile.TemporaryDirectory() as path:
            project_path = os.path.join(path, "project")
            shutil.copytree(
                os.path.join(self.sample_path, "configured-project"), project_path
            )
            cmd_configure(project_path)
            with open(os.path.join(project_path, "configuration.yaml")) as file:
                conf = yaml.safe_load(file)
                self.assertEqual(conf, {"host": "0.0.0.0", "namespaces": ["test-ns"]})

    @mock.patch("krsh.cmd.cmd_configure.icon_prompt")
    def test_cmd_configure_when_not_configured(self, mock_icon_prompt):
        mock_icon_prompt.side_effect = ["1.1.1.1", "happy-ns"]
        with tempfile.TemporaryDirectory() as path:
            project_path = os.path.join(path, "project")
            shutil.copytree(
                os.path.join(self.sample_path, "not-configured-project"), project_path
            )
            cmd_configure(project_path)
            with open(os.path.join(project_path, "configuration.yaml")) as file:
                conf = yaml.safe_load(file)
                self.assertEqual(conf, {"host": "1.1.1.1", "namespaces": ["happy-ns"]})
