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


def icon_echo(
    icon: str,
    text: str,
    fg: str,
    nl: bool = True,
    bold: bool = False,
    indent: int = 0,
    err: bool = False,
) -> None:
    """
    Print text with icon.

    Args:
        icon: Prefix icon of text
        text: to be printed text
        fg: text color
        nl: new line
        bold: print bold text
        indent: num of white space
        err: if this print is error, enter `True`
    """

    click.echo(click.style(f"{''*indent}{icon} ", fg=fg, bold=bold), nl=False)
    click.echo(click.style(text, bold=bold), nl=nl, err=err)


def icon_prompt(icon: str, text: str, fg: str, bold: bool = False) -> str:
    return click.prompt(
        click.style(f"{icon} ", fg=fg, bold=bold) + click.style(text, bold=bold)
    )


def ok_echo(text: str) -> None:
    """
    Positive echo with OK sign

    Args:
        text: to be printed text
    """

    icon_echo("OK", text, fg="green", err=False)


def nope_echo(text: str) -> None:
    """
    Negative echo with OK sign

    Args:
        text: to be printed text
    """

    icon_echo("NOPE", text, fg="red", err=True)


def create_diff_echo(name: str, namespace: str) -> None:
    """
    Print the pipeline to be created.

    Args:
        name: name of pipeline
        namespace: name of namespace
    """

    icon_echo("+", f"{namespace}.{name}", fg="green", bold=False, indent=4)


def destroy_diff_echo(name: str, namespace: str) -> None:
    """
    Print the pipeline to be destroyed.

    Args:
        name: name of pipeline
        namespace: name of namespace
    """

    icon_echo("-", f"{namespace}.{name}", fg="red", bold=False, indent=4)


def change_diff_echo(name: str, namespace: str) -> None:
    """
    Print the pipeline to be changed.

    Args:
        name: name of pipeline
        namespace: name of namespace
    """

    icon_echo("~", f"{namespace}.{name}", fg="yellow", bold=False, indent=4)
