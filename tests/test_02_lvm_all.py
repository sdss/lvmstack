# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-15
# @Filename: test_lvm_all.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


import pytest

import json

from click.testing import CliRunner

from clu import AMQPClient, AMQPActor, command_parser
from clu.tools import CommandStatus
from clu.model import Model
import logging

import container


lvm_all = 'lvm.all'
lvm_all_started_by_me = False

lvm_sci_foc = 'lvm.sci.foc'
lvm_sci_km = 'lvm.sci.km'
lvm_skye_foc = 'lvm.skye.foc'
lvm_skye_km = 'lvm.skye.km'
lvm_skyw_foc = 'lvm.skyw.foc'
lvm_skyw_km = 'lvm.skyw.km'
lvm_spec_foc = 'lvm.spec.foc'
lvm_spec_fibsel = 'lvm.spec.fibsel'


@pytest.fixture
async def clients():
    global lvm_all_started_by_me
    
    if not container.isRunning(lvm_all):
        print(f"Start own container {lvm_all}")
        runner = CliRunner()
        result = runner.invoke(container.start, ['--with_ui', '--name',  'lvm.all'])
        assert result.exit_code == 0
        lvm_all_started_by_me = True

    lvm_svcs = { 
            lvm_sci_foc: None, 
            lvm_sci_km: None,
            lvm_skye_foc: None,
            lvm_skye_km: None,
            lvm_skyw_foc: None,
            lvm_skyw_km: None,
            lvm_spec_foc: None,
            lvm_spec_fibsel: None }
    
    for name in lvm_svcs:
        client = AMQPClient(name=name + ".client", models=[name])
        await client.start()
        lvm_svcs[name] = client
   
    yield lvm_svcs

    for name in lvm_svcs:
        client = lvm_svcs[name]
        await client.stop()


async def client_send_command_blocking(clients: {}, name: str, cmd: str, *args):
    future =  await clients[name].send_command(name, cmd, *args)
    return await future


async def client_send_command_async(clients: {}, name: str, cmd: str, *args):
    return await clients[name].send_command(name, cmd, *args)
    

@pytest.mark.asyncio
async def test_getSchema(clients):
    for svc_name in dict(list(clients.items())):
        cmd = await client_send_command_blocking(clients, svc_name, 'get_schema')
        schema = json.loads(cmd.replies[-1].body["schema"])
        assert schema["additionalProperties"] == False
        assert(schema["properties"]['AtLimit']["type"] == 'boolean')
        assert(schema["properties"]['AtHome']["type"] == 'boolean')
        assert(schema["properties"]['Moving']["type"] == 'boolean')
        assert(schema["properties"]['Velocity']["type"] == 'number')
        assert(schema["properties"]['DeviceEncoderPosition']["type"] == 'number')
        assert(schema["properties"]['Position']["type"] == 'number')


@pytest.mark.asyncio
async def test_isAtLimit(clients):
    futures = {}
    for limit in [-1, 1]:
        for svc_name in dict(list(clients.items())[:-1]):
            futures[svc_name] = await client_send_command_async(clients, svc_name, 'movetolimit', limit)
        for svc_name in dict(list(clients.items())[:-1]):
            cmd = await futures[svc_name]
            assert(cmd.status == CommandStatus.DONE)    
            assert(cmd.replies[-1].body['AtLimit'] == True)

        for svc_name in dict(list(clients.items())[:-1]):
            cmd = await client_send_command_blocking(clients, svc_name, 'isatlimit')
            assert(cmd.status == CommandStatus.DONE)
            assert(cmd.replies[-1].body['AtLimit'] == True)


@pytest.mark.asyncio
async def test_isAtHome(clients):
    futures = {}
    for svc_name in dict(list(clients.items())[:-1]):
        futures[svc_name] = await client_send_command_async(clients, svc_name, 'movetohome')
    for svc_name in dict(list(clients.items())[:-1]):
        cmd = await futures[svc_name]
        assert(cmd.status == CommandStatus.DONE)    
        assert(cmd.replies[-1].body['AtHome'] == True)

    for svc_name in dict(list(clients.items())[:-1]):
        cmd = await client_send_command_blocking(clients, svc_name, 'isathome')
        assert(cmd.status == CommandStatus.DONE)
        assert(cmd.replies[-1].body['AtHome'] == True)


def test_shutdown(clients):
    if lvm_all_started_by_me and container.isRunning(lvm_all):
        runner = CliRunner()
        result = runner.invoke(container.stop, ['--name',  'lvm.all'])
        assert result.exit_code == 0
