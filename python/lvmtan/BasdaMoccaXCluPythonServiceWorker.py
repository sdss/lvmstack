# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-15
# @Filename: BasdaMoccaXCluPythonServiceWorker.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


import numpy as np
import Nice
import BasdaService
import BasdaMoccaException
import BasdaMoccaX

from .BasdaMoccaCluPythonServiceWorker import *


class BasdaMoccaXCluPythonServiceWorker(BasdaMoccaCluPythonServiceWorker):
   'python clu x worker'

   def __init__(self, _svcName):
      BasdaMoccaCluPythonServiceWorker.__init__(self, _svcName)


   @command_parser.command()
   @BasdaCluPythonServiceWorker.wrapper
   async def getAbsoluteEncoderPosition(self, command: Command):
        return command.finish(AbsoluteEncoderPosition=self.service.getAbsoluteEncoderPosition())
      
   @command_parser.command()
   @BasdaCluPythonServiceWorker.wrapper
   async def getIncrementalEncoderPosition(self, command: Command):
        return command.finish(IncrementalEncoderPosition=self.service.getIncrementalEncoderPosition())
      
   @command_parser.command()
   @BasdaCluPythonServiceWorker.wrapper
   async def getCurrentTime(self, command: Command):
        return command.finish(CurrentTime=self.service.getCurrentTime())
      
   @command_parser.command()
   @BasdaCluPythonServiceWorker.wrapper
   async def isAtLimit(self, command: Command):
        return command.finish(AtLimit=self.service.isAtLimit())
     
   @command_parser.command()
   @click.argument("LIMIT", type=int)
   @click.argument('UNITS', type=str, default='STEPS')
   @BasdaCluPythonServiceWorker.wrapper
   async def moveToLimit(self, command: Command, limit: int, units: str):
        if (limit == -1):
            command.info(text="move to negative")
        elif (limit == 1):
            command.info(text="move to positive")
        else:
            command.finish()
        self.service.moveToLimitStart(limit)
        while not self.service.moveToLimitCompletion().isDone():
            await asyncio.sleep(0.1)
            
            command.info( 
               DeviceEncoderPosition = self.service.getDeviceEncoderPosition(units),
               Units=units,
               Velocity = self.service.getVelocity(),
            )
        self.service.moveToLimitWait()

        return command.finish(
            AtLimit=self.service.isAtLimit(), 
            DeviceEncoderPosition = self.service.getDeviceEncoderPosition(units), 
            Units=units
        )
      
