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

from .BasdaMoccaBaseCluPythonServiceWorker import *


class BasdaMoccaXYCluPythonServiceWorker(BasdaMoccaBaseCluPythonServiceWorker):
   'python clu xy worker'

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
      
   @command_parser.command()
   @BasdaCluPythonServiceWorker.wrapper
   async def getAbsoluteEncoderPositionXY(self, command: Command):
        p = self.service.getAbsoluteEncoderPosition()
        return command.finish(AbsoluteEncoderPosition_X=p.x(), AbsoluteEncoderPosition_Y=p.y())

   @command_parser.command()
   @click.argument('UNITS', type=str, default='STEPS')
   @BasdaCluPythonServiceWorker.wrapper
   async def getPositionXY(self, command: Command, units: str):
        Nice.N_LOG("Hello world")
        p = self.service.getPosition(units)
        return command.finish(Position_X=p.x(), Position_Y=p.y(), Units=units)
      
   @command_parser.command()
   @click.argument("POSITIONX", type=int)
   @click.argument("POSITIONY", type=int)
   @BasdaCluPythonServiceWorker.wrapper
   async def setPositionXY(self, command: Command, position_x: int, position_y: int):
        self.service.setPosition(Nice.NPoint(position_x, position_y))
        return command.finish()
      
   @command_parser.command()
   @click.argument('UNITS', type=str, default='STEPS')
   @BasdaCluPythonServiceWorker.wrapper
   async def getDeviceEncoderPositionXY(self, command: Command, units: str):
        Nice.N_LOG("Hello world")
        p = self.service.getDeviceEncoderPosition(units)
        return command.finish(
            DeviceEncoderPosition_X=p.x(), 
            DeviceEncoderPosition_Y=p.y(), 
            Units=units)
      
   @command_parser.command()
   @BasdaCluPythonServiceWorker.wrapper
   async def getVelocityXY(self, command: Command):
        return command.finish(Velocity=self.service.getVelocity())
      
   @command_parser.command()
   @click.argument("VELOCITYX", type=int)
   @click.argument("VELOCITYY", type=int)
   @BasdaCluPythonServiceWorker.wrapper
   async def setVelocityXY(self, command: Command, velocity_x: int, velocity_y: int):
        self.service.setVelocity(velocity)
        return command.finish()
      
   @command_parser.command()
   @click.argument("NAMEDPOSITION", type=int)
   @BasdaCluPythonServiceWorker.wrapper
   async def getNamedPositionXY(self, command: Command, namedposition: int):
     try:
        p = self.service.getNamedPosition(namedposition)
        return command.finish(NamedPosition_X=p.x(), NamedPosition_Y=p.y())
     except Basda.Exception as e:
        E_LOG(e)         
     except Nice.Exception as e:
        E_LOG(e)         
     except Exception as e:
        E_LOG(traceback.format_exception(*sys.exc_info()))
      
   @command_parser.command()
   @click.argument("POSITIONX", type=int)
   @click.argument("POSITIONY", type=int)
   @click.argument('UNITS', type=str, default='STEPS')
   @BasdaCluPythonServiceWorker.wrapper
   async def moveRelativeXY(self, command: Command, position_x: int, position_y: int, units: str):
        self.service.moveRelativeStart(Nice.NPoint(position_x, position_y), units)
        while not self.service.moveRelativeCompletion().isDone():
            await asyncio.sleep(0.1)
            p = self.service.getDeviceEncoderPosition(units)
            vp = self.getVelocity(units)
            command.info(
                DeviceEncoderPosition_X = p.x(), 
                DeviceEncoderPosition_Y = p.y(), 
                Units=units,
                Velocity_X = vp.x(),
                Velocity_Y = vp.y()
            )
        self.service.moveRelativeWait()

        p = self.service.getDeviceEncoderPosition(units)
        return command.finish(
            DeviceEncoderPosition_X = p.x(), 
            DeviceEncoderPosition_Y = p.y(), 
            Units=units
        )
      
   @command_parser.command()
   @click.argument("POSITIONX", type=int)
   @click.argument("POSITIONY", type=int)
   @click.argument('UNITS', type=str, default='STEPS')
   @BasdaCluPythonServiceWorker.wrapper
   async def moveAbsoluteXY(self, command: Command, position_x: int, position_y: int, units: str):
        self.service.moveAbsoluteStart(position, units)
        while not self.service.moveAbsoluteCompletion().isDone():
            await asyncio.sleep(0.1)
            p = self.service.getDeviceEncoderPosition(units)
            vp = self.getVelocity(units)
            command.info(
                DeviceEncoderPosition_X = p.x(), 
                DeviceEncoderPosition_Y = p.y(), 
                Units=units,
                Velocity_X = vp[0],
                Velocity_Y = vp[1]
            )
        self.service.moveAbsoluteWait()

        p = self.service.getDeviceEncoderPosition(units)
        return command.finish(
            DeviceEncoderPosition_X = p.x(), 
            DeviceEncoderPosition_Y = p.y(), 
            Units=units
        )
      
   @command_parser.command()
   @click.argument("NAMEDPOSITION", type=int)
   @BasdaCluPythonServiceWorker.wrapper
   async def moveToNamedPositionXY(self, command: Command, namedposition: int):
        self.service.moveToNamedPositionStart(namedposition)
        while not self.service.moveToNamedPositionCompletion().isDone():
            await asyncio.sleep(0.1)
            p = self.service.getDeviceEncoderPosition(units)
            v = self.getVelocity(units)
            command.info(
                DeviceEncoderPosition_X = p.x(), 
                DeviceEncoderPosition_Y = p.y(), 
                Units=units,
                Velocity_X = v.x(),
                Velocity_Y = v.y()
            )

        self.service.moveToNamedPositionWait()

        return command.finish(NamedPosition=self.service.getNamedPosition(namedposition))

   @command_parser.command()
   @BasdaCluPythonServiceWorker.wrapper
   async def getIncrementalEncoderPositionXY(self, command: Command):
        p = self.service.getIncrementalEncoderPosition(units)
        return command.finish(IncrementalEncoderPosition_X = p.x(), IncrementalEncoderPosition_Y = p.y())
      
   @command_parser.command()
   @BasdaCluPythonServiceWorker.wrapper
   async def isAtLimitXY(self, command: Command):
        p = self.service.getDeviceEncoderPosition(units)
        return command.finish(AtLimit_X=p.x(), AtLimit_Y=p.y())

   @command_parser.command()
   @click.argument("LIMITX", type=int)
   @click.argument("LIMITY", type=int)
   @click.argument('UNITS', type=str, default='STEPS')
   @BasdaCluPythonServiceWorker.wrapper
   async def moveToLimitXY(self, command: Command, limit_x: int, limit_y: int, units: str):
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
            
            p = self.service.getDeviceEncoderPosition(units)
            command.info(
                DeviceEncoderPosition_X = p.x(), 
                DeviceEncoderPosition_Y = p.y(), 
                Units=units,
                Velocity = self.service.getVelocity(),
            )
        self.service.moveToLimitWait()

        
        p = self.service.getDeviceEncoderPosition(units)
        return command.finish(
            DeviceEncoderPosition_X = p.x(), 
            DeviceEncoderPosition_Y = p.y(), 
            AtLimit=self.service.isAtLimit(), 
            Units=units
        )
      
   @command_parser.command()
   @click.argument('UNITS', type=str, default='STEPS')
   @BasdaCluPythonServiceWorker.wrapper
   async def moveToHomeXY(self, command: Command, units: str):
        self.service.moveToHomeStart()
        while not self.service.moveToHomeCompletion().isDone():
            await asyncio.sleep(0.1)
            p = self.service.getDeviceEncoderPosition(units)
            command.info(
                DeviceEncoderPosition_X = p.x(), 
                DeviceEncoderPosition_Y = p.y(), 
                Units=units,
                Velocity = self.service.getVelocity()
            )
        self.service.moveToHomeWait()

        p = self.service.getDeviceEncoderPosition(units)
        return command.finish(
            DeviceEncoderPosition_X = p.x(), 
            DeviceEncoderPosition_Y = p.y(), 
            AtHome=self.service.isAtHome(),
            Units=units
        )
      
   @command_parser.command()
   @click.argument("NAMEDPOSITION", type=int)
   @BasdaCluPythonServiceWorker.wrapper
   async def moveToNamedPositionXY(self, command: Command, namedposition: int):
        self.service.moveToNamedPositionStart(namedposition)
        while not self.service.moveToNamedPositionCompletion().isDone():
            await asyncio.sleep(0.1)
            p = self.service.getDeviceEncoderPosition(units)
            command.info(
                DeviceEncoderPosition_X = p.x(), 
                DeviceEncoderPosition_Y = p.y(), 
                Units=units,
                Velocity = self.service.getVelocity()
            )

        self.service.moveToNamedPositionWait()

        p = self.service.getDeviceEncoderPosition(units)
        return command.finish(
                DeviceEncoderPosition_X = p.x(), 
                DeviceEncoderPosition_Y = p.y(), 
                NamedPosition=self.service.getNamedPosition(namedposition))


