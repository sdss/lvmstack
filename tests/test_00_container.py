# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-15
# @Filename: test_container.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import pytest

from click.testing import CliRunner
import container

@pytest.mark.slow
def test_container_build():
    runner = CliRunner()
    result = runner.invoke(container.build)
    assert result.exit_code == 0

