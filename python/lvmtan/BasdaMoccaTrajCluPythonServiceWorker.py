# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-15
# @Filename: BasdaMoccaTrajCluPythonServiceWorker.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


import datetime

import BasdaMoccaException
import BasdaMoccaTraj
import BasdaService
import Nice
import numpy as np

from .BasdaMoccaXCluPythonServiceWorker import *


class BasdaMoccaTrajCluPythonServiceWorker(BasdaMoccaXCluPythonServiceWorker):
    "python clu worker"

    def __init__(self, _svcName):
        BasdaMoccaXCluPythonServiceWorker.__init__(self, _svcName)

    @command_parser.command("changeProfile")
    @click.argument("START_DATE", type=datetime.datetime)
    #   @click.argument('POSITIONS', cls=ConvertStrToList, type=list)
    @click.argument("POSITIONS", type=list)
    @BasdaCluPythonServiceWorker.wrapper
    async def changeProfile(self, start_date: datetime.datetime, positions: list):
        """Change active trajectory"""
        # U8_LOG("changeProfile %s %s %s" % (start_date, positions, type(self.service)))
        try:
            self.service.changeProfile(Nice.Date.now(), Nice.NPoint(Nice.NPoint(positions)))
        except Exception as e:
            command.fail(error=e)

    @command_parser.command("startProfile")
    @click.argument("START_DATE", type=datetime.datetime)
    @click.argument("POSITIONS", type=list)
    @click.argument("FREQUENCY", type=int)
    @click.argument("SAMPLES_PER_SEGMENT", type=int)
    @click.argument("MAX_ERROR", type=int)
    @BasdaCluPythonServiceWorker.wrapper
    async def startProfile(
        self,
        start_date: datetime.datetime,
        positions: list,
        frequency: int,
        samples_per_segment: int,
        max_error: int,
    ):
        """Start trajectory"""
        # U8_LOG("startProfile %s %s %s %s %s" % (start_date, positions, frequency, samples_per_segment, max_error))
        try:
            self.service.startProfileStart(
                Nice.Date.fromUTC(
                    start_date.year,
                    start_date.month,
                    start_date.day,
                    start_date.hour,
                    start_date.minute,
                    start_date.second,
                    start_date.microsecond * 1000,
                ),
                Nice.NPoint(Nice.NPoint(positions)),
                frequency,
                samples_per_segment,
                max_error,
            )
            while not self.service.startProfileCompletion().isDone():
                await asyncio.sleep(0.01)
            self.service.startProfileWait()
        except Exception as e:
            command.fail(error=e)
