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

import click
import colorama

from krsh.cmd.cmd_apply import cmd_apply
from krsh.cmd.cmd_configure import cmd_configure
from krsh.cmd.cmd_plan import cmd_plan
from krsh.cmd.group_create.cmd_component import cmd_create_component
from krsh.cmd.group_create.cmd_pipeline import cmd_create_pipeline
from krsh.cmd.group_create.cmd_project import cmd_create_project


@click.group("krsh")
def cli():
    """
    Entrypoint of KRSH CLI.
    """

    colorama.init()


@cli.command("apply")
@click.argument("root", required=False, default=".")
@click.option("-mp", "--multiprocessing", "mp")
def apply(root, mp):
    """
    Entrypoint of KRSH Apply Command.
    """

    cmd_apply(root, mp)


@cli.command("plan")
@click.argument("root", required=False, default=".")
def plan(root):
    """
    Entrypoint of KRSH Plan Command.
    """

    cmd_plan(root)


@cli.command("configure")
@click.argument("root", required=False, default=".")
def configure(root):
    """
    Entrypoint of KRSH Configure Command.
    """
    cmd_configure(root)


@cli.group("create")
def create():
    """
    Command Group of Create Command.
    """

    pass


@create.command("project")
@click.argument("name", required=True)
@click.option("--root", required=False, default=".")
def create_project(name, root):
    """
    Entrypoint of create project command.
    """

    cmd_create_project(root, name)


@create.command("pipeline")
@click.argument("name", required=True)
@click.option("--namespace", "-ns", required=True)
@click.option("--root", required=False, default=".")
def create_pipeline(name, namespace, root):
    """
    Entrypoint of create pipeline command.
    """

    cmd_create_pipeline(root, name, namespace)


@create.command("component")
@click.argument("name", required=True)
@click.option("--root", required=False, default=".")
def create_component(name, root):
    """
    Entrypoint of create component command.
    """

    cmd_create_component(root, name)
