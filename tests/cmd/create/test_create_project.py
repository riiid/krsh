import os
import unittest
import tempfile

from krsh.cmd.group_create.cmd_project import cmd_create_project


class TestCommandCreateProject(unittest.TestCase):
    def test_create_project(self):
        with tempfile.TemporaryDirectory() as path:
            project_name = "test-project"
            cmd_create_project(path, project_name)
            project_root_path = os.path.join(path, project_name)

            self.assertTrue(project_root_path)
            self.assertTrue(os.path.join(project_root_path, "pipelines"))
            self.assertTrue(os.path.join(project_root_path, "components"))
            self.assertTrue(os.path.join(project_root_path, "dockerfiles"))
