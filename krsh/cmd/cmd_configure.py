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
import os
from yaml import dump
from yaml import safe_load

from krsh.config import PROJECT_CONFIG_FNAME
from krsh.cmd.io import icon_prompt
from krsh.cmd.io import ok_echo


def cmd_configure(root) -> None:
    """
    Implementation of Configure Command.

    Args:
        root: Project Path
    """

    path = os.path.join(root, PROJECT_CONFIG_FNAME)
    conf = {"host": None, "namespaces": None}
    # Input a configuration value
    conf["host"] = icon_prompt("?", "Host Address", fg="green")

    conf["namespaces"] = icon_prompt("?", "Namespaces", fg="green")
    conf["namespaces"] = list(map(lambda x: x.strip(), conf["namespaces"].split(",")))

    # Save a `configuration.yaml`
    with open(path, "w") as file:
        dump(
            {"host": conf["host"], "namespaces": conf["namespaces"]},
            file,
            default_flow_style=False,
        )
    click.echo()
    ok_echo("Configuration is configured successfully")
