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

import click

from krsh.cmd.io import ok_echo


def cmd_create_project(root: str, name: str):
    """
    Implementation of Create Project Command.

    Args:
        root: Project Path
        name: Name of Project
    """

    project_root = os.path.join(root, name)
    create_project_dir(project_root)
    create_pipelines_dir(project_root)
    create_components_dir(project_root)
    create_dockerfiles_dir(project_root)
    ok_echo(f"'{name}' project is created successfully")


def create_project_dir(path: str) -> None:
    try:
        os.mkdir(path)
    except FileExistsError:
        abspath = os.path.join(os.getcwd(), path)
        click.echo(f"{abspath} is already exists.")
        raise click.Abort()


def create_pipelines_dir(path: str) -> None:
    os.mkdir(os.path.join(path, "pipelines"))


def create_components_dir(path: str) -> None:
    os.mkdir(os.path.join(path, "components"))


def create_dockerfiles_dir(path: str) -> None:
    os.mkdir(os.path.join(path, "dockerfiles"))
