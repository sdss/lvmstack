# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-15
# @Filename: BasdaMoccaWheelCluPythonServiceWorker.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


import numpy as np
import Nice
import BasdaService
import BasdaMoccaException
import BasdaMoccaX

from .BasdaMoccaCluPythonServiceWorker import *

class BasdaMoccaWheelCluPythonServiceWorker(BasdaMoccaCluPythonServiceWorker):
   'python clu worker'

   def __init__(self, _svcName):
      BasdaMoccaCluPythonServiceWorker.__init__(self, _svcName)

   @command_parser.command()
   @BasdaCluPythonServiceWorker.wrapper
   async def scanAllReferenceSwitches(self):
       self.service.scanAllReferenceSwitchesStart()
       while not self.service.scanAllReferenceSwitchestCompletion().isDone():
            command.info( 
               DeviceEncoderPosition = self.service.getDeviceEncoderPosition(),
               Velocity = self.service.getVelocity(),
            )
       self.service.scanAllReferenceSwitchesWait()
       return command.finish(
            AtLimit=self.service.isAtLimit(), 
            DeviceEncoderPosition = self.service.getDeviceEncoderPosition(), 
         )
     
