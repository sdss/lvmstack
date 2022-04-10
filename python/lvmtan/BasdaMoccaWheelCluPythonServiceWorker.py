# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-15
# @Filename: BasdaMoccaWheelCluPythonServiceWorker.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


import BasdaMoccaException
import BasdaMoccaX
import BasdaService
import Nice
import numpy as np

from .BasdaMoccaCluPythonServiceWorker import *


class BasdaMoccaWheelCluPythonServiceWorker(BasdaMoccaCluPythonServiceWorker):
    "python clu worker"

    def __init__(self, _svcName):
        BasdaMoccaCluPythonServiceWorker.__init__(self, _svcName)


    @command_parser.command("scanAllReferenceSwitches")
    @BasdaCluPythonServiceWorker.wrapper
    async def scanAllReferenceSwitches(self):
        """Scan all reference switches"""
        try:
            self.service.scanAllReferenceSwitchesStart()
            while not self.service.scanAllReferenceSwitchestCompletion().isDone():
                command.info(
                    Position=self.service.getPosition(),
                    DeviceEncoder={"Position": self.service.getDeviceEncoderPosition("STEPS"), "Unit": "STEPS"},
                    Velocity=self.service.getVelocity(),
                    AtHome=self.service.isAtHome(),
                    AtLimit=self.service.isAtLimit(),
                )
            self.service.scanAllReferenceSwitchesWait()
            return command.finish(**self._status())

        except Exception as e:
            command.fail(error=e)
