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


class BasdaMoccaBaseCluPythonServiceWorker(BasdaCluPythonServiceWorker):
    "python clu worker"

    def __init__(self, _svcName):
        BasdaCluPythonServiceWorker.__init__(self, _svcName)
        self.schema["properties"]["AtLimit"] = {"type": "boolean"}
        self.schema["properties"]["AtHome"] = {"type": "boolean"}
        self.schema["properties"]["Moving"] = {"type": "boolean"}
        self.schema["properties"]["Reachable"] = {"type": "boolean"}
        self.schema["properties"]["CurrentTime"] = {"type": "number"}

    @command_parser.command()
    @BasdaCluPythonServiceWorker.wrapper
    async def isReachable(self, command: Command):
        return command.finish(Reachable=self.service.isReachable())

    @command_parser.command()
    @BasdaCluPythonServiceWorker.wrapper
    async def getPositionSwitchStatus(self, command: Command):
        return command.finish(
            PositionSwitchStatus=self.service.getPositionSwitchStatus()[0].getValue()
        )

    @command_parser.command()
    @BasdaCluPythonServiceWorker.wrapper
    async def isAtHome(self, command: Command):
        return command.finish(AtHome=self.service.isAtHome())

    @command_parser.command()
    @BasdaCluPythonServiceWorker.wrapper
    async def isMoving(self, command: Command):
        return command.finish(Moving=self.service.isMoving())

    @command_parser.command()
    @BasdaCluPythonServiceWorker.wrapper
    async def getCurrentTime(self, command: Command):
        return command.finish(CurrentTime=self.service.getCurrentTime())
