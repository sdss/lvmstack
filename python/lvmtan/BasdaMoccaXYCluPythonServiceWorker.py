# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-15
# @Filename: BasdaMoccaXYCluPythonServiceWorker.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


import numpy as np
import Nice
import BasdaService
import BasdaMoccaException
import BasdaMoccaXY

from .BasdaCluPythonServiceWorker import *


class BasdaMoccaXYCluPythonServiceWorker(BasdaCluPythonServiceWorker):
   'python clu x worker'

   def __init__(self, _svcName):
      BasdaCluPythonServiceWorker.__init__(self, _svcName)
      self.schema["properties"]["Position_X"] = {"type": "number"}
      self.schema["properties"]["Position_Y"] = {"type": "number"}
      self.schema["properties"]["DeviceEncoderPosition_X"] = {"type": "number"}
      self.schema["properties"]["DeviceEncoderPosition_Y"] = {"type": "number"}
      self.schema["properties"]["AtLimit_X"] = {"type": "boolean"}
      self.schema["properties"]["AtLimit_Y"] = {"type": "boolean"}
      self.schema["properties"]["Velocity_X"] = {"type": "number"}
      self.schema["properties"]["Velocity_Y"] = {"type": "number"}
      self.schema["properties"]["AtHome"] = {"type": "boolean"}
      self.schema["properties"]["Moving"] = {"type": "boolean"}
      self.schema["properties"]["PositionSwitchStatus_X"] = {"type": "number"}
      self.schema["properties"]["PositionSwitchStatus_Y"] = {"type": "number"}
      self.schema["properties"]["NamedPosition"] = {"type": "number"}
      self.schema["properties"]["Reachable"] = {"type": "boolean"}
      
   @command_parser.command()
   @BasdaCluPythonServiceWorker.wrapper
   async def getAbsoluteEncoderPosition(self, command: Command):
        np = self.service.getAbsoluteEncoderPosition()
        return command.finish(AbsoluteEncoderPosition_X=np[0], AbsoluteEncoderPosition_Y=np[1])

   @command_parser.command()
   @BasdaCluPythonServiceWorker.wrapper
   async def isReachable(self, command: Command):
        return command.finish(Reachable=self.service.isReachable())
      
   @command_parser.command()
   @click.argument('UNITS', type=str, default='STEPS')
   @BasdaCluPythonServiceWorker.wrapper
   async def getPosition(self, command: Command, units: str):
        np = self.service.getPosition(units)
        return command.finish(PositionX=np[0], PositionY=np[1], Units=units)
      
   @command_parser.command()
   @click.argument("POSITION_X", type=int)
   @click.argument("POSITION_Y", type=int)
   @BasdaCluPythonServiceWorker.wrapper
   async def setPosition(self, command: Command, position_x: int, position_y: int):
        self.service.setPosition(Nice.NPoint(position_x, position_y))
        return command.finish()
      
   @command_parser.command()
   @click.argument('UNITS', type=str, default='STEPS')
   @BasdaCluPythonServiceWorker.wrapper
   async def getDeviceEncoderPosition(self, command: Command, units: str):
        np = self.service.getDeviceEncoderPosition(units)
        return command.finish(DeviceEncoderPosition_X=np[0], DeviceEncoderPosition_Y=np[1], Units=units)
      
   @command_parser.command()
   @BasdaCluPythonServiceWorker.wrapper
   async def getVelocity(self, command: Command):
        return command.finish(Velocity=self.service.getVelocity())
      
   @command_parser.command()
   @click.argument("VELOCITY_X", type=int)
   @click.argument("VELOCITY_Y", type=int)
   @BasdaCluPythonServiceWorker.wrapper
   async def setVelocity(self, command: Command, velocity_x: int, velocity_y: int):
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
        np = self.service.getNamedPosition(namedposition)
        return command.finish(NamedPosition_X=np[0], NamedPosition_Y=np[1])
     except Basda.Exception as e:
        E_LOG(e)         
     except Nice.Exception as e:
        E_LOG(e)         
     except Exception as e:
        E_LOG(traceback.format_exception(*sys.exc_info()))
      
   @command_parser.command()
   @click.argument("POSITION_X", type=int)
   @click.argument("POSITION_Y", type=int)
   @click.argument('UNITS', type=str, default='STEPS')
   @BasdaCluPythonServiceWorker.wrapper
   async def moveRelative(self, command: Command, position_x: int, position_y: int, units: str):
        self.service.moveRelativeStart(Nice.NPoint(position_x, position_y), units)
        while not self.service.moveRelativeCompletion().isDone():
            await asyncio.sleep(0.1)
            np = self.service.getDeviceEncoderPosition(units)
            vp = self.getVelocity(units)
            command.info(
                DeviceEncoderPosition_X = np[0], 
                DeviceEncoderPosition_Y = np[1], 
                Units=units,
                Velocity_X = vp[0],
                Velocity_Y = vp[1]
            )
        self.service.moveRelativeWait()

        np = self.service.getDeviceEncoderPosition(units)
        return command.finish(
            DeviceEncoderPosition_X = np[0], 
            DeviceEncoderPosition_Y = np[1], 
            Units=units
        )
      
   @command_parser.command()
   @click.argument("POSITION", type=int)
   @click.argument('UNITS', type=str, default='STEPS')
   @BasdaCluPythonServiceWorker.wrapper
   async def moveAbsolute(self, command: Command, position: int, units: str):
        self.service.moveAbsoluteStart(position, units)
        while not self.service.moveAbsoluteCompletion().isDone():
            await asyncio.sleep(0.1)
            np = self.service.getDeviceEncoderPosition(units)
            vp = self.getVelocity(units)
            command.info(
                DeviceEncoderPosition_X = np[0], 
                DeviceEncoderPosition_Y = np[1], 
                Units=units,
                Velocity_X = vp[0],
                Velocity_Y = vp[1]
            )
        self.service.moveAbsoluteWait()

        np = self.service.getDeviceEncoderPosition(units)
        return command.finish(
            DeviceEncoderPosition_X = np[0], 
            DeviceEncoderPosition_Y = np[1], 
            Units=units
        )
      
   @command_parser.command()
   @click.argument('UNITS', type=str, default='STEPS')
   @BasdaCluPythonServiceWorker.wrapper
   async def moveToHome(self, command: Command, units: str):
        self.service.moveToHomeStart()
        while not self.service.moveToHomeCompletion().isDone():
            await asyncio.sleep(0.1)
            np = self.service.getDeviceEncoderPosition(units)
            vp = self.getVelocity(units)
            command.info(
                DeviceEncoderPosition_X = np[0], 
                DeviceEncoderPosition_Y = np[1], 
                Units=units,
                Velocity_X = vp[0],
                Velocity_Y = vp[1]
            )
        self.service.moveToHomeWait()

        np = self.service.getDeviceEncoderPosition(units)
        return command.finish(
            DeviceEncoderPosition_X = np[0], 
            DeviceEncoderPosition_Y = np[1], 
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
            np = self.service.getDeviceEncoderPosition(units)
            vp = self.getVelocity(units)
            command.info(
                DeviceEncoderPosition_X = np[0], 
                DeviceEncoderPosition_Y = np[1], 
                Units=units,
                Velocity_X = vp[0],
                Velocity_Y = vp[1]
            )

        self.service.moveToNamedPositionWait()

        return command.finish(NamedPosition=self.service.getNamedPosition(namedposition))

   @command_parser.command()
   @BasdaCluPythonServiceWorker.wrapper
   async def getIncrementalEncoderPosition(self, command: Command):
        np = self.service.getIncrementalEncoderPosition(units)
        return command.finish(IncrementalEncoderPosition_X = np[0], IncrementalEncoderPosition_Y = np[1])
      
   @command_parser.command()
   @BasdaCluPythonServiceWorker.wrapper
   async def getCurrentTime(self, command: Command):
        return command.finish(CurrentTime=self.service.getCurrentTime())
      
   @command_parser.command()
   @BasdaCluPythonServiceWorker.wrapper
   async def isAtLimit(self, command: Command):
        np = self.service.getDeviceEncoderPosition(units)
        return command.finish(AtLimit_X=np[0], AtLimit_Y=np[1])

   @command_parser.command()
   @click.argument("LIMIT_X", type=int)
   @click.argument("LIMIT_Y", type=int)
   @click.argument('UNITS', type=str, default='STEPS')
   @BasdaCluPythonServiceWorker.wrapper
   async def moveToLimit(self, command: Command, limit_x: int, limit_y: int, units: str):
        if (limit_x == -1):
            command.info(text="move to negative x")
        elif (limit_x == 1):
            command.info(text="move to positive x")
        else:
            limit_x = 0
            
        if (limit_y == -1):
            command.info(text="move to negative y")
        elif (limit_y == 1):
            command.info(text="move to positive y")
        else:
            limit_y = 0
            
        if limit_x == 0 and limit_y == 0:     
            command.finish()
        self.service.moveToLimitStart(Nice.NPoint(limit_x, limit_y))
        while not self.service.moveToLimitCompletion().isDone():
            await asyncio.sleep(0.1)
            
            np = self.service.getDeviceEncoderPosition(units)
            command.info(
                DeviceEncoderPosition_X = np[0], 
                DeviceEncoderPosition_Y = np[1], 
                Units=units,
                Velocity = self.service.getVelocity(),
            )
        self.service.moveToLimitWait()

        
        np = self.service.getDeviceEncoderPosition(units)
        return command.finish(
            DeviceEncoderPosition_X = np[0], 
            DeviceEncoderPosition_Y = np[1], 
            AtLimit=self.service.isAtLimit(), 
            Units=units
        )
      
