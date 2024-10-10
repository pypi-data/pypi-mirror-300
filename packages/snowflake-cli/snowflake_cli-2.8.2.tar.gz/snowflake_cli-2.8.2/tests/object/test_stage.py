# Copyright (c) 2024 Snowflake Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest


@pytest.mark.parametrize("command", ["copy", "create", "diff", "list", "remove"])
def test_object_stage_commands_cause_a_warning(command, runner):
    result = runner.invoke(["object", "stage", command, "--help"])
    assert result.exit_code == 0, result.output
    assert "(deprecated)" in result.output


def test_object_stage_main_command_causes_a_warning(runner):
    result = runner.invoke(["object", "stage", "--help"])
    assert result.exit_code == 0, result.output
    assert "(deprecated)" in result.output
