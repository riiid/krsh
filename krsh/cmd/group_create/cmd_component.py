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

import click

from krsh.cmd.io import ok_echo


def cmd_create_component(root: str, name: str) -> None:
    """
    Implementation of Create Component Command.

    Args:
        root: Project Path
        name: Name of Component
    """

    components_path = os.path.join(root, "components")
    if not os.path.exists(components_path):
        click.echo(
            "No such for directory 'components/'. "
            "Please execute the command at project root",
            err=True,
        )
        raise click.Abort()
    path = os.path.join(components_path, name)
    init_fname = "__init__.py"
    comp_fname = "component.py"
    init_py_tpl = pkgutil.get_data(
        __name__, os.path.join("templates/component", init_fname)
    ).decode("utf-8")
    comp_py_tpl = pkgutil.get_data(
        __name__, os.path.join("templates/component", comp_fname)
    ).decode("utf-8")
    os.mkdir(path)
    with open(os.path.join(path, init_fname), "w") as file:
        file.write(init_py_tpl.format(name=name))
    with open(os.path.join(path, comp_fname), "w") as file:
        file.write(comp_py_tpl.format(name=name))
    ok_echo(f"'{name}' component is created successfully")
