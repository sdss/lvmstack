# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-15
# @Filename: BasdaMoccaBaseCluPythonServiceWorker.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


import BasdaMoccaException
import BasdaMoccaX
import BasdaService
import Nice
import numpy as np
import json
from asyncio import sleep
from Basda import ServiceIsBusyException

from .BasdaCluPythonServiceWorker import (BasdaCluPythonServiceWorker, Command,
                                          asyncio, click, command_parser)


# TODO: use cluplus
@command_parser.command(name='__commands')
@click.pass_context
def __commands(ctx, command: Command):
    """Returns all commands."""

    # we have to use the help key for the command list, dont want to change the standard model.
    command.finish(help=[k for k in ctx.command.commands.keys() if k[:2] != '__'])



class BasdaMoccaBaseCluPythonServiceWorker(BasdaCluPythonServiceWorker):
    "python clu worker"

    def __init__(self, _svcName):
        BasdaCluPythonServiceWorker.__init__(self, _svcName)
        self.schema["properties"]["AtLimit"] = {"type": "boolean"}
        self.schema["properties"]["AtHome"] = {"type": "boolean"}
        self.schema["properties"]["Moving"] = {"type": "boolean"}
        self.schema["properties"]["Reachable"] = {"type": "boolean"}
        self.schema["properties"]["CurrentTime"] = {"type": "number"}
        self.schema["properties"]["ChatRc"] = {"type": "string"}
    
    @command_parser.command()
    @BasdaCluPythonServiceWorker.wrapper
    async def abort(self, command: Command):
        """Abort running command"""
        return command.finish(Reachable=self.service.abort())

    @command_parser.command()
    @BasdaCluPythonServiceWorker.wrapper
    async def stop(self, command: Command):
        """Stop running command gracefully"""
        return command.finish(Reachable=self.service.stop())

    @command_parser.command("isReachable")
    @BasdaCluPythonServiceWorker.wrapper
    async def isReachable(self, command: Command):
        """Check hardware reachability"""
        try:
            return command.finish(
                Reachable=self.service.isReachable()
            )
        except Exception as e:
            command.fail(error=e)

    @command_parser.command("getPositionSwitchStatus")
    @BasdaCluPythonServiceWorker.wrapper
    async def getPositionSwitchStatus(self, command: Command):
        """Returns position switches status"""
        try:
            return command.finish(
                PositionSwitchStatus=self.service.getPositionSwitchStatus()[0].getValue()
            )
        except Exception as e:
            command.fail(error=e)

    @command_parser.command("isAtHome")
    @BasdaCluPythonServiceWorker.wrapper
    async def isAtHome(self, command: Command):
        """Check if at home position"""
        try:
            return command.finish(
                AtHome=self.service.isAtHome()
            )
        except Exception as e:
            command.fail(error=e)

    @command_parser.command("isMoving")
    @BasdaCluPythonServiceWorker.wrapper
    async def isMoving(self, command: Command):
        """Check if moving"""
        try:
            return command.finish(
                Moving=self.service.isMoving()
            )
        except Exception as e:
            command.fail(error=e)

    @command_parser.command("getCurrentTime")
    @BasdaCluPythonServiceWorker.wrapper
    async def getCurrentTime(self, command: Command):
        """Returns internal time counter"""
        try:
            return command.finish(
                    CurrentTime=self.service.getCurrentTime()
                )
        except Exception as e:
            command.fail(error=e)

    @command_parser.command("chat")
    @click.argument("CARD", type=int)
    @click.argument("COM", type=int)
    @click.argument("MODULE", type=int)
    @click.argument("SELECT", type=int, default=0)
    @click.argument("PARAMS", type=str, default="")
    @click.argument("LINES", type=int, default=0)
    @BasdaCluPythonServiceWorker.wrapper
    async def chat(self, command: Command, card: int, com: int, module: int, select: int, params: str, lines: int):
        """Check hardware reachability"""
        try:
            try:  
                self.service.send(str(card),str(com),str(module),str(select),str(params),str(lines))
                await asyncio.sleep(0.01)
                rc = self.service.receive().split('\n')

            except ServiceIsBusyException as ex:
                Nice.W_LOG("got busy exception - wait and try again")
                await asyncio.sleep(0.4)
                self.service.send(str(card),str(com),str(module),str(select),str(params),str(lines))
                await asyncio.sleep(0.01)
                rc = self.service.receive().split('\n')

            if int(rc[-1].split(' ')[3]) < 0:
                command.fail(error=Exception(f"Error #{rc[-1]}"))

        except Exception as e:
            command.fail(error=e)

        return command.finish(
              ChatRc = json.dumps(rc[:-1])
        )

