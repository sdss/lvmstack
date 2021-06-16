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

from container import *


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

lvm_svcs = None

@pytest.fixture
async def clients():
    global lvm_all_started_by_me

    if not cntr_isRunning(lvm_all):
        print(f"Start own container {lvm_all}")
        runner = CliRunner()
        result = runner.invoke(cntr_run, ['--with_ui'])
        assert result.exit_code == 0
        lvm_all_started_by_me = True
    print("Start connecting")
    if not lvm_svcs:
        global lvm_svcs = { 
                lvm_sci_foc: None, 
                lvm_sci_km: None,
                lvm_skye_foc: None,
                lvm_skye_km: None,
                lvm_skyw_foc: None,
                lvm_skyw_km: None,
                lvm_spec_foc: None,
                lvm_spec_fibsel: None }
        for key in lvm_svcs:
        print(f"Start {key}")
        client = AMQPClient(name=key + ".client")
        await client.start()
        yield client
        lvm_svcs[key] = client
        print(lvm_svcs)

    #for key in lvm_svcs:
       #await lvm_svcs[key].stop()
    

async def client_send_command(svc: str, cmd, *args):
    print("sendcommand")
    future =  await lvm_svcs[svc].send_command(svc, cmd, *args)
    return await future
    

#@pytest.mark.asyncio
#async def test_getSchema(client):
    #cmd = await client_send_command(client, 'get_schema')
    #schema = json.loads(cmd.replies[-1].body["schema"])
    #assert schema["additionalProperties"] == False
    #assert(schema["properties"]['AtLimit']["type"] == 'boolean')
    #assert(schema["properties"]['AtHome']["type"] == 'boolean')
    #assert(schema["properties"]['Moving']["type"] == 'boolean')
    #assert(schema["properties"]['Velocity']["type"] == 'number')
    #assert(schema["properties"]['DeviceEncoderPosition']["type"] == 'number')
    #assert(schema["properties"]['Position']["type"] == 'number')


@pytest.mark.asyncio
async def test_isAtLimit(clients):
    for svc_name in dict(list(lvm_svcs.items())[:-1]):
        print(svc_name)
        #for limit in [-1, 1]:
            #cmd = await client_send_command(svc_name, 'movetolimit', limit)
            #assert(cmd.status == CommandStatus.DONE)    
            #assert(cmd.replies[-1].body['AtLimit'] == True)
            #cmd = await client_send_command(svc_name, 'isatlimit')
            #assert(cmd.status == CommandStatus.DONE)
            #assert(cmd.replies[-1].body['AtLimit'] == True)
            #assert(client.models[lvm_all]['AtLimit'].value == True)

#@pytest.mark.asyncio
#async def test_isAtHome(client):
    #cmd = await client_send_command(client, 'isathome')
    #assert(cmd.status == CommandStatus.DONE)
    #if not cmd.replies[-1].body['AtHome']:
        #print(f"moving ...")
        #cmd = await client_send_command(client, 'movetohome')
        #assert(cmd.status == CommandStatus.DONE)    
        #assert(cmd.replies[-1].body['AtHome'] == True)

   
def test_shutdown():
    if lvm_all_started_by_me and cntr_isRunning(lvm_all):
        runner = CliRunner()
        result = runner.invoke(cntr_kill)
        assert result.exit_code == 0
    for key in lvm_svcs:
        await lvm_svcs[key].stop()
 
