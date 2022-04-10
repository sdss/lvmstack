# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-15
# @Filename: BasdaMoccaXYCluPythonServiceWorker.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


import BasdaMoccaException
import BasdaMoccaXY
import BasdaService
import Nice
import numpy as np

from .BasdaMoccaBaseCluPythonServiceWorker import *


class BasdaMoccaXYCluPythonServiceWorker(BasdaMoccaBaseCluPythonServiceWorker):
    "python clu xy worker"

    def __init__(self, _svcName):
        BasdaMoccaBaseCluPythonServiceWorker.__init__(self, _svcName)
        self.schema["properties"]["Position_X"] = {"type": "number"}
        self.schema["properties"]["Position_Y"] = {"type": "number"}
        self.schema["properties"]["DeviceEncoderPosition_X"] = {"type": "number"}
        self.schema["properties"]["DeviceEncoderPosition_Y"] = {"type": "number"}
        self.schema["properties"]["AtLimit_X"] = {"type": "boolean"}
        self.schema["properties"]["AtLimit_Y"] = {"type": "boolean"}
        self.schema["properties"]["Velocity_X"] = {"type": "number"}
        self.schema["properties"]["Velocity_Y"] = {"type": "number"}
        self.schema["properties"]["PositionSwitchStatus_X"] = {"type": "number"}
        self.schema["properties"]["PositionSwitchStatus_Y"] = {"type": "number"}
        self.schema["properties"]["NamedPosition_X"] = {"type": "number"}
        self.schema["properties"]["NamedPosition_Y"] = {"type": "number"}
        self.schema["properties"]["AbsoluteEncoderPosition_X"] = {"type": "number"}
        self.schema["properties"]["AbsoluteEncoderPosition_Y"] = {"type": "number"}

    @command_parser.command("getAbsoluteEncoderPositionXY")
    @BasdaCluPythonServiceWorker.wrapper
    async def getAbsoluteEncoderPositionXY(self, command: Command):
        try:
            p = self.service.getAbsoluteEncoderPosition()
            return command.finish(
                AbsoluteEncoderPosition_X=p.x(), AbsoluteEncoderPosition_Y=p.y()
            )
        except Exception as e:
            command.fail(error=e)

    @command_parser.command("getPositionXY")
    @click.argument("UNIT", type=str, default="")
    @BasdaCluPythonServiceWorker.wrapper
    async def getPositionXY(self, command: Command, units: str):
        unit = unit if len(unit) else self.unit
        try:
            Nice.N_LOG("Hello world")
            p = self.service.getPosition(units)
            return command.finish(Position_X=p.x(), Position_Y=p.y(), Units=units)
        except Exception as e:
            command.fail(error=e)


    @command_parser.command("setPositionXY")
    @click.argument("POSITION_X", type=float)
    @click.argument("POSITION_Y", type=float)
    @BasdaCluPythonServiceWorker.wrapper
    async def setPositionXY(
        self, command: Command, position_x: float, position_y: float
    ):
        try:
            self.service.setPosition(Nice.NPoint(position_x, position_y))
            return command.finish()
        except Exception as e:
            command.fail(error=e)

    @command_parser.command("getDeviceEncoderPositionXY")
    @click.argument("UNIT", type=str, default="")
    @BasdaCluPythonServiceWorker.wrapper
    async def getDeviceEncoderPositionXY(self, command: Command, units: str):
        unit = unit if len(unit) else self.unit
        try:
            p = self.service.getDeviceEncoderPosition(units)
            return command.finish(
                DeviceEncoderPosition_X=p.x(), DeviceEncoderPosition_Y=p.y(), Units=units
            )
        except Exception as e:
            command.fail(error=e)

    @command_parser.command("getVelocityXY")
    @BasdaCluPythonServiceWorker.wrapper
    async def getVelocityXY(self, command: Command):
        try:
            vp = self.service.getVelocity()
            return command.finish(Velocity_X=vp.x(), Velocity_Y=vp.y())
        except Exception as e:
            command.fail(error=e)

    @command_parser.command("setVelocityXY")
    @click.argument("VELOCITY_X", type=float)
    @click.argument("VELOCITY_Y", type=float)
    @BasdaCluPythonServiceWorker.wrapper
    async def setVelocityXY(
        self, command: Command, velocity_x: float, velocity_y: float
    ):
        try:
            vp = self.service.getVelocity()
            self.service.setVelocity(velocity)
            return command.finish()
        except Exception as e:
            command.fail(error=e)

    @command_parser.command("getNamedPositionXY")
    @click.argument("NAMEDPOSITION", type=int)
    @BasdaCluPythonServiceWorker.wrapper
    async def getNamedPositionXY(self, command: Command, namedposition: int):
        try:
            p = self.service.getNamedPosition(namedposition)
            return command.finish(NamedPosition_X=p.x(), NamedPosition_Y=p.y())
        except Exception as e:
            command.fail(error=e)

    @command_parser.command("moveRelativeXY")
    @click.argument("POSITION_X", type=float)
    @click.argument("POSITION_Y", type=float)
    @click.argument("UNIT", type=str, default="")
    @BasdaCluPythonServiceWorker.wrapper
    async def moveRelativeXY(
        self, command: Command, position_x: float, position_y: float, units: str
    ):
        unit = unit if len(unit) else self.unit
        try:  
            self.service.moveRelativeStart(Nice.Point(position_x, position_y), units)
            while not self.service.moveRelativeCompletion().isDone():
                await asyncio.sleep(0.1)
                p = self.service.getDeviceEncoderPosition(units)
                vp = self.service.getVelocity()
                command.info(
                    DeviceEncoderPosition_X=p.x(),
                    DeviceEncoderPosition_Y=p.y(),
                    Units=units,
                    Velocity_X=vp.x(),
                    Velocity_Y=vp.y(),
                )

            self.service.moveRelativeWait()

            p = self.service.getDeviceEncoderPosition(units)
            return command.finish(
                DeviceEncoderPosition_X=p.x(), DeviceEncoderPosition_Y=p.y(), Units=units
            )
        except Exception as e:

    @command_parser.command("moveAbsoluteXY")
    @click.argument("POSITION_X", type=float)
    @click.argument("POSITION_Y", type=float)
    @click.argument("UNIT", type=str, default="")
    @BasdaCluPythonServiceWorker.wrapper
    async def moveAbsoluteXY(
        self, command: Command, position_x: float, position_y: float, units: str
    ):
        unit = unit if len(unit) else self.unit
        try:
            self.service.moveAbsoluteStart(Nice.Point(position_x, position_y), units)
            while not self.service.moveAbsoluteCompletion().isDone():
                await asyncio.sleep(0.1)
                p = self.service.getDeviceEncoderPosition(units)
                vp = self.service.getVelocity()
                command.info(
                    DeviceEncoderPosition_X=p.x(),
                    DeviceEncoderPosition_Y=p.y(),
                    Units=units,
                    Velocity_X=vp.x(),
                    Velocity_Y=vp.y(),
                )

            self.service.moveAbsoluteWait()

            p = self.service.getDeviceEncoderPosition(units)
            return command.finish(
                DeviceEncoderPosition_X=p.x(), DeviceEncoderPosition_Y=p.y(), Units=units
            )
        except Exception as e:

    @command_parser.command("moveToNamedPositionXY")
    @click.argument("NAMEDPOSITION", type=int)
    @BasdaCluPythonServiceWorker.wrapper
    async def moveToNamedPositionXY(self, command: Command, namedposition: int):
        try:
            self.service.moveToNamedPositionStart(namedposition)
            while not self.service.moveToNamedPositionCompletion().isDone():
                await asyncio.sleep(0.1)
                p = self.service.getDeviceEncoderPosition(units)
                v = self.service.getVelocity()
                command.info(
                    DeviceEncoderPosition_X=p.x(),
                    DeviceEncoderPosition_Y=p.y(),
                    Units=units,
                    Velocity_X=v.x(),
                    Velocity_Y=v.y(),
                )

            self.service.moveToNamedPositionWait()

            return command.finish(
                NamedPosition=self.service.getNamedPosition(namedposition)
            )
        except Exception as e:

    @command_parser.command("getIncrementalEncoderPositionXY")
    @BasdaCluPythonServiceWorker.wrapper
    async def getIncrementalEncoderPositionXY(self, command: Command):
        p = self.service.getIncrementalEncoderPosition(units)
        return command.finish(
            IncrementalEncoderPosition_X=p.x(), IncrementalEncoderPosition_Y=p.y()
        )

    @command_parser.command("isAtLimitXY")
    @BasdaCluPythonServiceWorker.wrapper
    async def isAtLimitXY(self, command: Command):
        p = self.service.getDeviceEncoderPosition(units)
        return command.finish(AtLimit_X=p.x(), AtLimit_Y=p.y())

    @command_parser.command("moveToLimitXY")
    @click.argument("LIMIT_X", type=int)
    @click.argument("LIMIT_Y", type=int)
    @click.argument("UNIT", type=str, default="")
    @BasdaCluPythonServiceWorker.wrapper
    async def moveToLimitXY(
        self, command: Command, limit_x: int, limit_y: int, units: str
    ):
        unit = unit if len(unit) else self.unit
        if limit_x == -1:
            command.info(text="move to negative x")
        elif limit_x == 1:
            command.info(text="move to positive x")
        else:
            limit_x = 0

        if limit_y == -1:
            command.info(text="move to negative y")
        elif limit_y == 1:
            command.info(text="move to positive y")
        else:
            limit_y = 0

        if limit_x == 0 and limit_y == 0:
            command.finish()
        self.service.moveToLimitStart(Nice.NPoint(limit_x, limit_y))

        while not self.service.moveToLimitCompletion().isDone():
            await asyncio.sleep(0.1)

            p = self.service.getDeviceEncoderPosition(units)
            v = self.service.getVelocity()
            command.info(
                DeviceEncoderPosition_X=p.x(),
                DeviceEncoderPosition_Y=p.y(),
                Units=units,
                Velocity_X=v.x(),
                Velocity_Y=v.y(),
            )
        self.service.moveToLimitWait()

        p = self.service.getDeviceEncoderPosition(units)
        return command.finish(
            DeviceEncoderPosition_X=p.x(),
            DeviceEncoderPosition_Y=p.y(),
            AtLimit=self.service.isAtLimit(),
            Units=units,
        )

    @command_parser.command("moveToHomeXY")
    @click.argument("UNIT", type=str, default="")
    @BasdaCluPythonServiceWorker.wrapper
    async def moveToHomeXY(self, command: Command, units: str):
        unit = unit if len(unit) else self.unit
        self.service.moveToHomeStart()
        while not self.service.moveToHomeCompletion().isDone():
            await asyncio.sleep(0.1)
            p = self.service.getDeviceEncoderPosition(units)
            v = self.service.getVelocity()
            command.info(
                DeviceEncoderPosition_X=p.x(),
                DeviceEncoderPosition_Y=p.y(),
                Units=units,
                Velocity_X=v.x(),
                Velocity_Y=v.y(),
            )
        self.service.moveToHomeWait()

        p = self.service.getDeviceEncoderPosition(units)
        return command.finish(
            DeviceEncoderPosition_X=p.x(),
            DeviceEncoderPosition_Y=p.y(),
            AtHome=self.service.isAtHome(),
            Units=units,
        )

    @command_parser.command("moveToNamedPositionXY")
    @click.argument("NAMEDPOSITION", type=int)
    @BasdaCluPythonServiceWorker.wrapper
    async def moveToNamedPositionXY(self, command: Command, namedposition: int):
        self.service.moveToNamedPositionStart(namedposition)
        while not self.service.moveToNamedPositionCompletion().isDone():
            await asyncio.sleep(0.1)
            p = self.service.getDeviceEncoderPosition(units)
            v = self.service.getVelocity()
            command.info(
                DeviceEncoderPosition_X=p.x(),
                DeviceEncoderPosition_Y=p.y(),
                Units=units,
                Velocity_X=v.x(),
                Velocity_Y=v.y(),
            )

        self.service.moveToNamedPositionWait()

        p = self.service.getDeviceEncoderPosition(units)
        return command.finish(
            DeviceEncoderPosition_X=p.x(),
            DeviceEncoderPosition_Y=p.y(),
            NamedPosition=self.service.getNamedPosition(namedposition),
        )
