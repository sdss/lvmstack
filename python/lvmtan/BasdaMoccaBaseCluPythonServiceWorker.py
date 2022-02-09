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

    @command_parser.command("isReachable")
    @BasdaCluPythonServiceWorker.wrapper
    async def isReachable(self, command: Command):
        """Check hardware reachability"""
        try:
            return command.finish(
                Reachable=reachable
            )
        except Exception as e:
            command.fail(error=e)

    @command_parser.command("status")
    @BasdaCluPythonServiceWorker.wrapper
    async def isReachable(self, command: Command):
        """Check hardware reachability"""
        try:
            units="STEPS"
            reachable = self.service.isReachable()
            return command.finish(
                Reachable=reachable,
                AtHome=self.service.isAtHome() if reachable else "Unknown",
                AtLimit=self.service.isAtLimit() if reachable else "Unknown",
                Moving=self.service.isMoving() if reachable else "Unknown",
                CurrentTime=self.service.getCurrentTime() if reachable else "Unknown",
                PositionSwitchStatus=self.service.getPositionSwitchStatus()[0].getValue() if reachable else "Unknown",
                DeviceEncoderPosition=self.service.getDeviceEncoderPosition(units) if reachable else "Unknown",
                Units=units if reachable else "Unknown",
                Velocity=self.service.getVelocity() if reachable else "Unknown",
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
