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

from krsh.cmd.plan import calculate_plan
from krsh.cmd.plan import parse_local_pipelines
from krsh.cmd.plan import parse_remote_pipelines
from krsh.cmd.plan import plan


def cmd_plan(root):
    """
    Implementation of Plan Command.

    Args:
        root: Project Path
    """

    local_pipelines = parse_local_pipelines(root)
    remote_pipelines = parse_remote_pipelines(root)
    planned = calculate_plan(local_pipelines, remote_pipelines)
    plan(planned)
