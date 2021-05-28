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

import os
import pkgutil
from typing import List

import click
import yaml

from krsh.config import PipelineConfig
from krsh.cmd.io import ok_echo


def cmd_create_pipeline(root, name: str, namespace: str) -> None:
    """
    Implementation of Create Pipeline Command.

    Args:
        root: Project Path
        name: Name of Pipeline
        namespace: Name of Namespace
    """

    pipelines_path = os.path.join(root, "pipelines")
    if not os.path.exists(pipelines_path):
        click.echo(
            "No such for directory 'pipelines/'. "
            "Please execute the command at project root",
            err=True,
        )
        raise click.Abort()
    path = os.path.join(pipelines_path, name)
    os.mkdir(path)

    py_fname = "pipeline.py"
    yml_fname = "pipeline.yaml"
    py_path = os.path.join(path, py_fname)
    yml_path = os.path.join(path, yml_fname)

    py_tpl = pkgutil.get_data(
        __name__, os.path.join("templates/pipeline", py_fname)
    ).decode("utf-8")

    with open(py_path, "w") as file:
        file.write(py_tpl.format(name=name))
    with open(yml_path, "w") as file:
        yml_tpl: PipelineConfig = {
            "name": name,
            "entry_point": "pipeline.py",
            "namespaces": parse_ns_str(namespace),
        }
        yaml.dump(yml_tpl, file, default_flow_style=False)

    ok_echo(f"'{name}' pipeline is created successfully")


def parse_ns_str(namespace: str) -> List[str]:
    return list(map(lambda x: x.strip(), namespace.split(",")))
