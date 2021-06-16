# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-15
# @Filename: BasdaMoccaCluPythonServiceWorker.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


import numpy as np
import Nice
import BasdaService
import BasdaMoccaException
import BasdaMoccaX

from .BasdaCluPythonServiceWorker import asyncio, click, command_parser, Command, BasdaCluPythonServiceWorker


class BasdaMoccaCluPythonServiceWorker(BasdaCluPythonServiceWorker):
   'python clu worker'

   def __init__(self, _svcName):
      BasdaCluPythonServiceWorker.__init__(self, _svcName)
      self.schema["properties"]["Position"] = {"type": "number"}
      self.schema["properties"]["DeviceEncoderPosition"] = {"type": "number"}
      self.schema["properties"]["AtLimit"] = {"type": "boolean"}
      self.schema["properties"]["Velocity"] = {"type": "number"}
      self.schema["properties"]["AtHome"] = {"type": "boolean"}
      self.schema["properties"]["Moving"] = {"type": "boolean"}
      self.schema["properties"]["PositionSwitchStatus"] = {"type": "number"}
      self.schema["properties"]["NamedPosition"] = {"type": "number"}
      
   @command_parser.command()
   @BasdaCluPythonServiceWorker.wrapper
   async def getAbsoluteEncoderPosition(self, command: Command):
        return command.finish(AbsoluteEncoderPosition=self.service.getAbsoluteEncoderPosition())

   @command_parser.command()
   @BasdaCluPythonServiceWorker.wrapper
   async def isReachable(self, command: Command):
        return command.finish(Reachable=self.service.isReachable())
      
   @command_parser.command()
   @click.argument('UNITS', type=str, default='STEPS')
   @BasdaCluPythonServiceWorker.wrapper
   async def getPosition(self, command: Command, units: str):
        return command.finish(Position=self.service.getPosition(units), Units=units)
      
   @command_parser.command()
   @click.argument("POSITION", type=int)
   @BasdaCluPythonServiceWorker.wrapper
   async def setPosition(self, command: Command, position: int):
        self.service.setPosition(position)
        return command.finish()
      
   @command_parser.command()
   @click.argument('UNITS', type=str, default='STEPS')
   @BasdaCluPythonServiceWorker.wrapper
   async def getDeviceEncoderPosition(self, command: Command, units: str):
        return command.finish(DeviceEncoderPosition=self.service.getDeviceEncoderPosition(units), Units=units)
      
   @command_parser.command()
   @BasdaCluPythonServiceWorker.wrapper
   async def getVelocity(self, command: Command):
        return command.finish(Velocity=self.service.getVelocity())
      
   @command_parser.command()
   @click.argument("VELOCITY", type=int)
   @BasdaCluPythonServiceWorker.wrapper
   async def setVelocity(self, command: Command, velocity: int):
        self.service.setVelocity(velocity)
        return command.finish()
      
   @command_parser.command()
   @BasdaCluPythonServiceWorker.wrapper
   async def getPositionSwitchStatus(self, command: Command):
        return command.finish(PositionSwitchStatus=self.service.getPositionSwitchStatus()[0].getValue())
      
   @command_parser.command()
   @BasdaCluPythonServiceWorker.wrapper
   async def isAtHome(self, command: Command):
        return command.finish(AtHome=self.service.isAtHome())
      
   @command_parser.command()
   @BasdaCluPythonServiceWorker.wrapper
   async def isMoving(self, command: Command):
        return command.finish(Moving=self.service.isMoving())
      
   @command_parser.command()
   @click.argument("NAMEDPOSITION", type=int)
   @BasdaCluPythonServiceWorker.wrapper
   async def getNamedPosition(self, command: Command, namedposition: int):
     try:
        return command.finish(NamedPosition=self.service.getNamedPosition(namedposition) )
     except Basda.Exception as e:
        E_LOG(e)         
     except Nice.Exception as e:
        E_LOG(e)         
     except Exception as e:
        E_LOG(traceback.format_exception(*sys.exc_info()))
      
   @command_parser.command()
   @click.argument("POSITION", type=int)
   @click.argument('UNITS', type=str, default='STEPS')
   @BasdaCluPythonServiceWorker.wrapper
   async def moveRelative(self, command: Command, position: int, units: str):
        self.service.moveRelativeStart(position, units)
        while not self.service.moveRelativeCompletion().isDone():
            await asyncio.sleep(0.1)
            command.info(
                DeviceEncoderPosition = self.service.getDeviceEncoderPosition(units), 
                Units=units,
                Velocity = self.service.getVelocity()
            )
        self.service.moveRelativeWait()

        return command.finish(DeviceEncoderPosition = self.service.getDeviceEncoderPosition(units), Units=units)
      
   @command_parser.command()
   @click.argument("POSITION", type=int)
   @click.argument('UNITS', type=str, default='STEPS')
   @BasdaCluPythonServiceWorker.wrapper
   async def moveAbsolute(self, command: Command, position: int, units: str):
        self.service.moveAbsoluteStart(position, units)
        while not self.service.moveAbsoluteCompletion().isDone():
            await asyncio.sleep(0.1)
            command.info(
                DeviceEncoderPosition = self.service.getDeviceEncoderPosition(units), 
                Units=units,
                Velocity = self.service.getVelocity()
            )
        self.service.moveAbsoluteWait()

        return command.finish(DeviceEncoderPosition = self.service.getDeviceEncoderPosition(units), Units=units)
      
   @command_parser.command()
   @click.argument('UNITS', type=str, default='STEPS')
   @BasdaCluPythonServiceWorker.wrapper
   async def moveToHome(self, command: Command, units: str):
        self.service.moveToHomeStart()
        while not self.service.moveToHomeCompletion().isDone():
            await asyncio.sleep(0.1)
            command.info(
                DeviceEncoderPosition = self.service.getDeviceEncoderPosition(units), 
                Units=units,
                Velocity = self.service.getVelocity()
            )
        self.service.moveToHomeWait()

        return command.finish(
            DeviceEncoderPosition = self.service.getDeviceEncoderPosition(units), 
            AtHome=self.service.isAtHome(),
            Units=units
        )
      
   @command_parser.command()
   @click.argument("NAMEDPOSITION", type=int)
   @BasdaCluPythonServiceWorker.wrapper
   async def moveToNamedPosition(self, command: Command, namedposition: int):
        self.service.moveToNamedPositionStart(namedposition)
        while not self.service.moveToNamedPositionCompletion().isDone():
            await asyncio.sleep(0.1)
            command.info(
                DeviceEncoderPosition = self.service.getDeviceEncoderPosition(units), 
                Units=units,
                Velocity = self.service.getVelocity()
            )

        self.service.moveToNamedPositionWait()

        return command.finish(NamedPosition=self.service.getNamedPosition(namedposition))

