import os
import shutil
import tempfile
import unittest

from krsh.cmd.group_create.cmd_component import cmd_create_component


class TestCommandCreateComponent(unittest.TestCase):
    def setUp(self):
        self.sample_path = os.path.join(os.path.dirname(__file__), "../../samples")

    def test_create_component(self):
        with tempfile.TemporaryDirectory() as path:
            project_path = os.path.join(path, "project")
            shutil.copytree(
                os.path.join(self.sample_path, "configured-project"), project_path
            )
            comp_name = "test_comp"
            components_path = os.path.join(project_path, "components")
            cmd_create_component(project_path, comp_name)
            self.assertTrue(os.path.exists(os.path.join(components_path, comp_name)))
            self.assertTrue(
                os.path.exists(os.path.join(components_path, comp_name, "component.py"))
            )
            self.assertTrue(
                os.path.exists(os.path.join(components_path, comp_name, "__init__.py"))
            )
