# Copyright 2021 AIOps Squad, Riiid Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc
import click
import hashlib
import importlib
import kfp
import os
import tempfile
from yaml import safe_load

from krsh.config import PipelineConfig
from krsh.config import get_pipeline_config
from krsh.kubeflow.client import get_client

COMPILED_FNAME = "compiled.yaml"
CONF_FNAME = "pipeline.yaml"


class Pipeline(metaclass=abc.ABCMeta):
    def __init__(self, name: str, namespace: str):
        self.name: str = name
        self.namespace: str = namespace
        self.client: kfp.Client = get_client(namespace)

    @abc.abstractmethod
    def get_identifier(self) -> str:
        pass


class LocalPipeline(Pipeline):
    def __init__(self, name: str, namespace: str):
        super(LocalPipeline, self).__init__(name, namespace)
        self.path: str = os.path.join("pipelines", self.name)
        self.config: PipelineConfig = get_pipeline_config(self.name)

    def get_identifier(self) -> str:
        with tempfile.TemporaryDirectory() as workdir:
            path = self.compile(workdir)
            with open(path) as file:
                data = safe_load(file)
                del data["metadata"]["annotations"][
                    "pipelines.kubeflow.org/pipeline_compilation_time"
                ]
                identifier = hashlib.md5(str(data).encode("utf-8"))
        return identifier.hexdigest()

    def compile(self, workdir: str) -> str:
        in_path = os.path.join(self.path, self.config["entry_point"])
        out_path = os.path.join(workdir, COMPILED_FNAME)

        spec = importlib.util.spec_from_file_location("pipe", in_path)
        pipe = importlib.util.module_from_spec(spec)
        name = in_path.split("/")[-2]
        try:
            spec.loader.exec_module(pipe)
        except Exception as e:
            click.echo(
                f"'{name}' pipeline cannot be compiled. Please refer to the error below.\n",
                err=True,
            )
            click.echo(e, err=True)
            raise click.Abort()
        kfp.compiler.Compiler().compile(pipe.pipeline, out_path)

        return out_path


class RemotePipeline(Pipeline):
    def __init__(self, name: str, namespace: str):
        super(RemotePipeline, self).__init__(name, namespace)
        self.pipeline = self.client.get_pipeline(self.client.get_pipeline_id(name))

    def get_identifier(self) -> str:
        return self.pipeline.default_version.name

    def get_pipeline_id(self) -> int:
        return self.pipeline.id


def upload_pipeline(pipeline: LocalPipeline) -> bool:
    with tempfile.TemporaryDirectory() as workdir:
        dsl_path = pipeline.compile(workdir)
        if pipeline.client.get_pipeline_id(pipeline.name) is None:
            pipeline.client.upload_pipeline(
                pipeline_package_path=dsl_path, pipeline_name=pipeline.name,
            )
        pipeline.client.upload_pipeline_version(
            pipeline_package_path=dsl_path,
            pipeline_version_name=pipeline.get_identifier(),
            pipeline_name=pipeline.name,
        )
    return True  # TODO: 실패구간 지정


def delete_pipeline(pipeline: RemotePipeline) -> bool:
    pid = pipeline.get_pipeline_id()
    pipeline.client.delete_pipeline(pid)
    return True  # TODO: 실패구간 지정
