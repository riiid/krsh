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

from multiprocessing import Pool
from typing import Any
from typing import Dict

import click

from krsh.kubeflow.pipeline import delete_pipeline
from krsh.kubeflow.pipeline import upload_pipeline
from krsh.cmd.plan import PlannedPipelines
from krsh.cmd.plan import calculate_plan
from krsh.cmd.plan import parse_local_pipelines
from krsh.cmd.plan import parse_remote_pipelines
from krsh.cmd.plan import plan
from krsh.cmd.plan import planned_pipelines_to_list


def cmd_apply(root, mp):
    """
    Implementation of Apply Command.

    Args:
        root: Project Path
        mp: run using multiprocessing
    """

    local_pipelines = parse_local_pipelines(root)
    remote_pipelines = parse_remote_pipelines(root)
    planned = calculate_plan(local_pipelines, remote_pipelines)

    if not plan(planned):
        return
    click.echo(click.style("Do you really want to these actions?", bold=True))
    enter = click.prompt(click.style("  Enter yes or no", bold=True))
    if enter != "yes":
        return
    click.echo()

    if mp:
        apply_multiprocessing(planned)
    else:
        apply_singleprocessing(planned)

    num_added = len(planned["to_be_added"])
    num_changed = len(planned["to_be_changed"])
    num_destroyed = len(planned["to_be_destroyed"])
    complete_str = f"Apply complete! Resource: {num_added} added, {num_changed} changed, {num_destroyed} destroyed."
    click.echo(click.style(complete_str, fg="green"))


def apply_single_pipeline(action_pipeline_dict: Dict[str, Any]) -> None:
    pipeline = action_pipeline_dict["pipeline"]
    action = action_pipeline_dict["action"]
    if action == "to_be_added" or action == "to_be_changed":
        upload_pipeline(pipeline)
    elif action == "to_be_destroyed":
        delete_pipeline(pipeline)

    action_str = ""
    if action == "to_be_added":
        action_str = "added"
    elif action == "to_be_changed":
        action_str = "changed"
    elif action == "to_be_destroyed":
        action_str = "destroyed"

    click.echo(f'"{pipeline.namespace}.{pipeline.name}" is {action_str}.')


def apply_multiprocessing(planned: PlannedPipelines):
    pipelines = planned_pipelines_to_list(planned)
    with Pool() as p:
        p.map(apply_single_pipeline, pipelines)
    click.echo()


def apply_singleprocessing(planned: PlannedPipelines):
    pipelines = planned_pipelines_to_list(planned)
    for action_pipeline_dict in pipelines:
        apply_single_pipeline(action_pipeline_dict)
    click.echo()
