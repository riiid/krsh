import os
import shutil
import tempfile
import unittest
from unittest import mock

from krsh.cmd.cmd_apply import cmd_apply


class MockPipeline:
    class Version:
        def __init__(self, name):
            self.name = name

    def __init__(self, name, id, default_version):
        self.name = name
        self.id = id
        self.default_version = MockPipeline.Version(default_version)


class MockKubeflowClient:
    class MockResponse:
        def __init__(self, pipelines):
            self.pipelines = pipelines
            self.next_page_token = None

    def __init__(self, namespace):
        super(MockKubeflowClient, self).__init__()
        self.namespace = namespace

    def get_pipeline_id(self, name):
        return name

    def get_pipeline(self, pid):
        return MockPipeline(pid, pid, pid)

    def set_user_namespace(self, namespace):
        self.namespace = namespace

    def get_user_namespace(self):
        return self.namespace

    def list_pipelines(self, token, page_size):
        return MockKubeflowClient.MockResponse(
            [
                MockPipeline("pipeline-2", "pipeline-2", "pipeline-2"),
                MockPipeline("pipeline-3", "pipeline-3", "pipeline-3"),
            ]
        )


class TestCommandApply(unittest.TestCase):
    def setUp(self):
        self.sample_path = os.path.join(os.path.dirname(__file__), "../samples")

    @mock.patch(
        "krsh.kubeflow.pipeline.get_client",
        return_value=MockKubeflowClient("test-ns-1"),
    )
    @mock.patch(
        "krsh.cmd.plan.get_client", return_value=MockKubeflowClient("test-ns-1")
    )
    @mock.patch("krsh.cmd.cmd_apply.click.prompt", return_value="yes")
    @mock.patch("krsh.cmd.cmd_apply.upload_pipeline", return_value=None)
    @mock.patch("krsh.cmd.cmd_apply.delete_pipeline", return_value=None)
    def test_cmd_apply(
        self,
        mock_get_client,
        mock_plan_get_client,
        mock_click_prompt,
        mock_upload_pipeline,
        mock_delete_pipeline,
    ):
        with tempfile.TemporaryDirectory() as path:
            project_path = os.path.join(path, "project")
            shutil.copytree(
                os.path.join(self.sample_path, "have-pipeline-project"), project_path
            )
            os.chdir(project_path)
            cmd_apply(project_path, mp=False)
