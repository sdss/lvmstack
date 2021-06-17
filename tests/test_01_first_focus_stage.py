# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-15
# @Filename: test_first_focus_stage.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


import pytest

import json

from click.testing import CliRunner

from clu import AMQPClient, AMQPActor, command_parser
from clu.tools import CommandStatus
from clu.model import Model
import logging

import container

test_first_focus_stage = 'test.first.focus_stage'
test_first_focus_stage_started_by_me = False


@pytest.fixture
async def client():
    global test_first_focus_stage_started_by_me
    if not container.isRunning(test_first_focus_stage):
        print(f"Start own container {test_first_focus_stage}")
        runner = CliRunner()
        result = runner.invoke(container.start, ['--with_ui'])
        assert result.exit_code == 0
        test_first_focus_stage_started_by_me = True

    client = AMQPClient(name=test_first_focus_stage + ".client", models=[test_first_focus_stage])
    await client.start()
    yield client
    await client.stop()
    

async def client_send_command(client, cmd, *args):
    future =  await client.send_command(test_first_focus_stage, cmd, *args)
    return await future


@pytest.mark.asyncio
async def test_getSchema(client):
    cmd = await client_send_command(client, 'get_schema')
    schema = json.loads(cmd.replies[-1].body["schema"])
    assert schema["additionalProperties"] == False
    assert(schema["properties"]['AtLimit']["type"] == 'boolean')
    assert(schema["properties"]['AtHome']["type"] == 'boolean')
    assert(schema["properties"]['Moving']["type"] == 'boolean')
    assert(schema["properties"]['Velocity']["type"] == 'number')
    assert(schema["properties"]['DeviceEncoderPosition']["type"] == 'number')
    assert(schema["properties"]['Position']["type"] == 'number')


@pytest.mark.asyncio
async def test_isAtLimit(client):
    for limit in [-1, 1]:
        cmd = await client_send_command(client, 'movetolimit', limit)
        assert(cmd.status == CommandStatus.DONE)    
        assert(cmd.replies[-1].body['AtLimit'] == True)

        cmd = await client_send_command(client, 'isatlimit')
        assert(cmd.status == CommandStatus.DONE)
        assert(cmd.replies[-1].body['AtLimit'] == True)
        assert(client.models[test_first_focus_stage]['AtLimit'].value == True)
        

@pytest.mark.asyncio
async def test_isAtHome(client):
    cmd = await client_send_command(client, 'isathome')
    assert(cmd.status == CommandStatus.DONE)
    if not cmd.replies[-1].body['AtHome']:
        cmd = await client_send_command(client, 'movetohome')
        assert(cmd.status == CommandStatus.DONE)    
        assert(cmd.replies[-1].body['AtHome'] == True)

   
def test_shutdown():
    if test_first_focus_stage_started_by_me and container.isRunning(test_first_focus_stage):
        runner = CliRunner()
        result = runner.invoke(container.stop)
        assert result.exit_code == 0
  
