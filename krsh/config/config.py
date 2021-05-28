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
from typing import List

import click
from typing_extensions import TypedDict
from yaml import safe_load

PROJECT_CONFIG_FNAME = "configuration.yaml"
PIPELINE_CONFIG_FNAME = "pipeline.yaml"


class ProjectConfig(TypedDict):
    host: str
    namespaces: List[str]


def get_project_config(root: str) -> ProjectConfig:
    path = os.path.join(root, PROJECT_CONFIG_FNAME)
    if not os.path.exists(path):
        click.echo(
            f"Could not found {PROJECT_CONFIG_FNAME}! "
            f"Run the command from the root of the project or 'krsh configure'",
            err=True,
        )
        raise click.Abort()
    with open(path) as file:
        return safe_load(file)


class PipelineConfig(TypedDict):
    name: str
    entry_point: str
    namespaces: List[str]


def get_pipeline_config(name: str) -> PipelineConfig:
    with open(os.path.join("pipelines", name, PIPELINE_CONFIG_FNAME)) as file:
        conf = safe_load(file)
    return conf
