import os
import shutil
import tempfile
import unittest

import yaml

from krsh.cmd.group_create.cmd_pipeline import cmd_create_pipeline


class TestCommandCreatePipeline(unittest.TestCase):
    def setUp(self):
        self.sample_path = os.path.join(os.path.dirname(__file__), "../../samples")

    def test_create_pipeline(self):
        with tempfile.TemporaryDirectory() as path:
            project_path = os.path.join(path, "project")
            shutil.copytree(
                os.path.join(self.sample_path, "configured-project"), project_path
            )
            cmd_create_pipeline(project_path, "test-pipeline", "test-ns1,test-ns2")
            self.assertTrue(
                os.path.exists(
                    os.path.join(project_path, "pipelines", "test-pipeline"),
                )
            )
            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        project_path, "pipelines", "test-pipeline", "pipeline.yaml"
                    )
                )
            )
            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        project_path, "pipelines", "test-pipeline", "pipeline.py"
                    )
                )
            )
            with open(
                os.path.join(
                    project_path, "pipelines", "test-pipeline", "pipeline.yaml"
                )
            ) as file:
                conf = yaml.safe_load(file)
                expected = {
                    "name": "test-pipeline",
                    "entry_point": "pipeline.py",
                    "namespaces": ["test-ns1", "test-ns2"],
                }
                self.assertEqual(expected, conf)
