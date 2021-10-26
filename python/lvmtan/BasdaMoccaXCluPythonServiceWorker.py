# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-15
# @Filename: BasdaMoccaXCluPythonServiceWorker.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


import BasdaMoccaException
import BasdaMoccaX
import BasdaService
import Nice
import numpy as np

from .BasdaMoccaCluPythonServiceWorker import *


class BasdaMoccaXCluPythonServiceWorker(BasdaMoccaCluPythonServiceWorker):
    "python clu x worker"

    def __init__(self, _svcName):
        BasdaMoccaCluPythonServiceWorker.__init__(self, _svcName)

    @command_parser.command("isAtLimit")
    @BasdaCluPythonServiceWorker.wrapper
    async def isAtLimit(self, command: Command):
       try:
           return command.finish(AtLimit=self.service.isAtLimit())
       except Exception as e:
            command.fail(error=e)

    @command_parser.command("moveToLimit")
    @click.argument("LIMIT", type=int)
    @click.argument("UNITS", type=str, default="STEPS")
    @BasdaCluPythonServiceWorker.wrapper
    async def moveToLimit(self, command: Command, limit: int, units: str):
        '''Move to positive/negative limit'''
        try:
            if limit == -1:
                command.info(text="move to negative")
            elif limit == 1:
                command.info(text="move to positive")
            else:
                command.finish()
            self.service.moveToLimitStart(limit)
            while not self.service.moveToLimitCompletion().isDone():
                await asyncio.sleep(0.1)

                command.info(
                    DeviceEncoderPosition=self.service.getDeviceEncoderPosition(units),
                    Units=units,
                    Velocity=self.service.getVelocity(),
                )
            self.service.moveToLimitWait()

            return command.finish(
                AtLimit=self.service.isAtLimit(),
                DeviceEncoderPosition=self.service.getDeviceEncoderPosition(units),
                Units=units,
            )
        except Exception as e:
            command.fail(error=e)
