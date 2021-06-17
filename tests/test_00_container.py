# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-15
# @Filename: test_container.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import pytest

from click.testing import CliRunner
from container import *

@pytest.mark.slow
def test_container_build():
    runner = CliRunner()
    result = runner.invoke(container_build)
    assert result.exit_code == 0


@pytest.mark.slow
def test_container_start():
    runner = CliRunner()
    result = runner.invoke(container_run, ['--without_ui'])
    assert result.exit_code == 0


@pytest.mark.slow
def test_container_stop():
    runner = CliRunner()
    result = runner.invoke(container_kill)
    assert result.exit_code == 0
