# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-15
# @Filename: BasdaMoccaCluPythonServiceWorker.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


import BasdaMoccaException
import BasdaMoccaX
import BasdaService
import Nice
import numpy as np

import traceback
import sys
import json

from .BasdaMoccaBaseCluPythonServiceWorker import *


class BasdaMoccaCluPythonServiceWorker(BasdaMoccaBaseCluPythonServiceWorker):
    "python clu worker"

    def __init__(self, _svcName):
        BasdaMoccaBaseCluPythonServiceWorker.__init__(self, _svcName)
        self.schema["properties"]["Position"] = {"type": "number"}
        self.schema["properties"]["DeviceEncoderPosition"] = {"type": "number"}
        self.schema["properties"]["IncrementalEncoderPosition"] = {"type": "number"}
        self.schema["properties"]["AbsoluteEncoderPosition"] = {"type": "number"}
        self.schema["properties"]["Velocity"] = {"type": "number"}
        self.schema["properties"]["PositionSwitchStatus"] = {"type": "number"}
        self.schema["properties"]["NamedPosition"] = {"type": "number"}

    @command_parser.command("getAbsoluteEncoderPosition")
    @BasdaCluPythonServiceWorker.wrapper
    async def getAbsoluteEncoderPosition(self, command: Command):
        """Returns external absolute encoder position if available"""
        return command.finish(
            AbsoluteEncoderPosition=self.service.getAbsoluteEncoderPosition()
        )

    @command_parser.command("getPosition")
    @click.argument("UNITS", type=str, default="STEPS")
    @BasdaCluPythonServiceWorker.wrapper
    async def getPosition(self, command: Command, units: str):
        """Returns internal motorcontroller position counter"""
        return command.finish(Position=self.service.getPosition(units), Units=units)

    @command_parser.command("setPosition")
    @click.argument("POSITION", type=int)
    @BasdaCluPythonServiceWorker.wrapper
    async def setPosition(self, command: Command, position: int):
        """Sets internal motorcontroller position counter"""
        self.service.setPosition(position)
        return command.finish()

    @command_parser.command("getDeviceEncoderPosition")
    @click.argument("UNITS", type=str, default="STEPS")
    @BasdaCluPythonServiceWorker.wrapper
    async def getDeviceEncoderPosition(self, command: Command, units: str):
        """Returns internal motorcontroller position counter in supplied  unit"""
        return command.finish(
            DeviceEncoderPosition=self.service.getDeviceEncoderPosition(units),
            Units=units,
        )

    @command_parser.command("getIncrementalEncoderPosition")
    @BasdaCluPythonServiceWorker.wrapper
    async def getIncrementalEncoderPosition(self, command: Command):
        """Returns external incremental encoder position if available"""
        return command.finish(
            IncrementalEncoderPosition=self.service.getIncrementalEncoderPosition()
        )

    @command_parser.command("getVelocity")
    @BasdaCluPythonServiceWorker.wrapper
    async def getVelocity(self, command: Command):
        """Returns current set velocity"""
        return command.finish(Velocity=self.service.getVelocity())

    @command_parser.command("getNamedPosition")
    @click.argument("NAMEDPOSITION", type=int)
    @BasdaCluPythonServiceWorker.wrapper
    async def getNamedPosition(self, command: Command, namedposition: int):
        """Returns named position"""
        try:
            return command.finish(
                NamedPosition=self.service.getNamedPosition(namedposition)
            )
        except Exception as e:
            command.fail(
                error=e.__repr__()
            )            

    @command_parser.command("setVelocity")
    @click.argument("VELOCITY", type=int)
    @BasdaCluPythonServiceWorker.wrapper
    async def setVelocity(self, command: Command, velocity: int):
        """Set velocity"""
        self.service.setVelocity(velocity)
        return command.finish()

    @command_parser.command("moveRelative")
    @click.argument("POSITION", type=float)
    @click.argument("UNITS", type=str, default="STEPS")
    @BasdaCluPythonServiceWorker.wrapper
    async def moveRelative(self, command: Command, position: float, units: str):
        """Move relative with unit"""
        self.service.moveRelativeStart(position, units)
        while not self.service.moveRelativeCompletion().isDone():
            await asyncio.sleep(0.1)
            command.info(
                DeviceEncoderPosition=self.service.getDeviceEncoderPosition(units),
                Units=units,
                Velocity=self.service.getVelocity(),
            )
        self.service.moveRelativeWait()

        return command.finish(
            DeviceEncoderPosition=self.service.getDeviceEncoderPosition(units),
            Units=units,
        )

    @command_parser.command("moveAbsolute")
    @click.argument("POSITION", type=float)
    @click.argument("UNITS", type=str, default="STEPS")
    @BasdaCluPythonServiceWorker.wrapper
    async def moveAbsolute(self, command: Command, position: float, units: str):
        """Move to absolute position with unit"""
        self.service.moveAbsoluteStart(position, units)
        while not self.service.moveAbsoluteCompletion().isDone():
            await asyncio.sleep(0.1)
            command.info(
                DeviceEncoderPosition=self.service.getDeviceEncoderPosition(units),
                Units=units,
                Velocity=self.service.getVelocity(),
            )
        self.service.moveAbsoluteWait()

        return command.finish(
            DeviceEncoderPosition=self.service.getDeviceEncoderPosition(units),
            Units=units,
        )

    @command_parser.command("moveToHome")
    @click.argument("UNITS", type=str, default="STEPS")
    @BasdaCluPythonServiceWorker.wrapper
    async def moveToHome(self, command: Command, units: str):
        """Move to home position"""
        self.service.moveToHomeStart()
        while not self.service.moveToHomeCompletion().isDone():
            await asyncio.sleep(0.1)
            command.info(
                DeviceEncoderPosition=self.service.getDeviceEncoderPosition(units),
                Units=units,
                Velocity=self.service.getVelocity(),
            )
        self.service.moveToHomeWait()

        return command.finish(
            DeviceEncoderPosition=self.service.getDeviceEncoderPosition(units),
            AtHome=self.service.isAtHome(),
            Units=units,
        )

    @command_parser.command("moveToNamedPosition")
    @click.argument("NAMEDPOSITION", type=float)
    @BasdaCluPythonServiceWorker.wrapper
    async def moveToNamedPosition(self, command: Command, namedposition: int):
        """Move to named position"""
        self.service.moveToNamedPositionStart(namedposition)
        while not self.service.moveToNamedPositionCompletion().isDone():
            await asyncio.sleep(0.1)
            command.info(
                DeviceEncoderPosition=self.service.getDeviceEncoderPosition(units),
                Units=units,
                Velocity=self.service.getVelocity(),
            )

        self.service.moveToNamedPositionWait()

        return command.finish(
            DeviceEncoderPosition=self.service.getDeviceEncoderPosition(units),
            NamedPosition=self.service.getNamedPosition(namedposition),
        )
