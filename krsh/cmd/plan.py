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

import glob
import os
from typing import Any
from typing import Dict
from typing import List

import click
from typing_extensions import TypedDict

from krsh.cmd.utils import is_pipeline_path
from krsh.config import PipelineConfig
from krsh.config import ProjectConfig
from krsh.config import get_pipeline_config
from krsh.config import get_project_config
from krsh.kubeflow import LocalPipeline
from krsh.kubeflow import RemotePipeline
from krsh.kubeflow import get_client


class PlannedPipelines(TypedDict):
    to_be_added: List[LocalPipeline]
    to_be_changed: List[LocalPipeline]
    to_be_destroyed: List[RemotePipeline]


def plan(planned: PlannedPipelines) -> bool:
    if planned["to_be_added"] or planned["to_be_changed"] or planned["to_be_destroyed"]:
        echo_planned_pipelines(planned)
        return True
    else:
        click.echo("No changes. Kubeflow is up-to-date.")
        return False


def calculate_plan(
    local_pipelines: List[LocalPipeline], remote_pipelines: List[RemotePipeline]
) -> PlannedPipelines:
    local_names_dict = {p.name: p for p in local_pipelines}
    remote_names_dict = {p.name: p for p in remote_pipelines}
    local_names_set = set(local_names_dict.keys())
    remote_names_set = set(remote_names_dict.keys())

    to_be_added = [
        local_names_dict[k] for k in list(local_names_set - remote_names_set)
    ]
    to_be_destroyed = [
        remote_names_dict[k] for k in list(remote_names_set - local_names_set)
    ]
    to_be_changed = [
        local_names_dict[k]
        for k in list(remote_names_set & local_names_set)
        if local_names_dict[k].get_identifier() != remote_names_dict[k].get_identifier()
    ]
    return {
        "to_be_added": to_be_added,
        "to_be_destroyed": to_be_destroyed,
        "to_be_changed": to_be_changed,
    }


def planned_pipelines_to_list(planned: PlannedPipelines) -> List[Dict[str, Any]]:
    ret = []
    for k in planned.keys():
        for pipeline in planned[k]:
            ret.append({"pipeline": pipeline, "action": k})
    return ret


def echo_planned_pipelines(planned: PlannedPipelines) -> None:
    click.echo("\nKRSH will perform following actions:\n")
    name_list = []
    for key in ("to_be_added", "to_be_destroyed", "to_be_changed"):
        for pipeline in planned[key]:
            name = f"{pipeline.name}.{pipeline.namespace}"
            echo = ""
            if key == "to_be_added":
                echo = trans_added_str(name)
            if key == "to_be_changed":
                echo = trans_changed_str(name)
            if key == "to_be_destroyed":
                echo = trans_destroyed_str(name)
            name_list.append({"name": name, "echo": echo})
    sorted(name_list, key=lambda x: x["name"])
    for n in name_list:
        click.echo(n["echo"])

    num_added = len(planned["to_be_added"])
    num_changed = len(planned["to_be_changed"])
    num_destroyed = len(planned["to_be_destroyed"])

    added_str = f"{num_added} to added"
    if num_added != 0:
        added_str = click.style(added_str, fg="green")

    changed_str = f"{num_changed} to changed"
    if num_changed != 0:
        changed_str = click.style(changed_str, fg="yellow")

    destroyed_str = f"{num_destroyed} to destroyed"
    if num_destroyed != 0:
        destroyed_str = click.style(destroyed_str, fg="red")
    click.echo(f"\nPlan: {added_str}, {changed_str}, {destroyed_str}\n")


def trans_added_str(name: str) -> str:
    return f'{click.style("+", fg="green")} pipeline "{name}"'


def trans_changed_str(name: str) -> str:
    return f'{click.style("~", fg="yellow")} pipeline "{name}"'


def trans_destroyed_str(name: str) -> str:
    return f'{click.style("-", fg="red")} pipeline "{name}"'


def parse_local_pipelines(root: str) -> List[LocalPipeline]:
    pipelines_path = os.path.join(root, "pipelines")
    pipeline_paths = list(filter(is_pipeline_path, glob.glob(pipelines_path + "/*")))
    names = list(map(os.path.basename, pipeline_paths))
    pipelines = []
    for name in names:
        config: PipelineConfig = get_pipeline_config(name)
        for ns in config["namespaces"]:
            pipelines.append(LocalPipeline(name=name, namespace=ns))
    return pipelines


def parse_remote_pipelines(root: str) -> List[RemotePipeline]:
    conf: ProjectConfig = get_project_config(root)
    pipelines = []
    for ns in conf["namespaces"]:
        client = get_client(ns)
        token = ""
        while token is not None:
            res = client.list_pipelines(token, page_size=50)
            if res.pipelines is None:
                break
            pipelines += [RemotePipeline(p.name, ns) for p in res.pipelines]
            token = res.next_page_token
    return pipelines
