# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-15
# @Filename: BasdaMoccaTrajCluPythonServiceWorker.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


import numpy as np
import datetime

import Nice
import BasdaService
import BasdaMoccaException
import BasdaMoccaTraj

from .BasdaMoccaXCluPythonServiceWorker import *


class BasdaMoccaTrajCluPythonServiceWorker(BasdaMoccaXCluPythonServiceWorker):
   'python clu worker'

   def __init__(self, _svcName):
       BasdaMoccaXCluPythonServiceWorker.__init__(self, _svcName)

   # not tested !
   class ConvertStrToList(click.Option):
       def type_cast_value(self, ctx, value) -> list:
           try:
               value = str(value)
               assert value.count('[') == 1 and value.count(']') == 1
               list_as_str = value.replace('"', "'").split('[')[1].split(']')[0]
               list_of_items = [item.strip().strip("'") for item in list_as_str.split(',')]
               return list_of_items
           except Exception:
               raise click.BadParameter(value)

   @command_parser.command()
   @click.argument("START_DATE", type=datetime.datetime)
#   @click.argument('POSITIONS', cls=ConvertStrToList, type=list)
   @click.argument('POSITIONS', type=list)
   @BasdaCluPythonServiceWorker.wrapper
   async def changeProfile(self, start_date: datetime.datetime, positions: list):
        #U8_LOG("changeProfile %s %s %s" % (start_date, positions, type(self.service)))
        self.service.changeProfile(Nice.Date.now(), Nice.NPoint(Nice.NPoint(positions)))
        
   @command_parser.command()
   @click.argument("START_DATE", type=datetime.datetime)
   @click.argument('POSITIONS', type=list)
   @click.argument("FREQUENCY", type=int)
   @click.argument("SAMPLES_PER_SEGMENT", type=int)
   @click.argument("MAX_ERROR", type=int)
   @BasdaCluPythonServiceWorker.wrapper
   async def startProfile(self, start_date: datetime.datetime, positions: list, frequency: int, samples_per_segment: int, max_error: int):
        #U8_LOG("startProfile %s %s %s %s %s" % (start_date, positions, frequency, samples_per_segment, max_error))
        try:
            self.service.startProfileStart(
                Nice.Date.fromUTC(start_date.year, start_date.month, start_date.day, start_date.hour, start_date.minute, start_date.second, start_date.microsecond*1000), 
                Nice.NPoint(Nice.NPoint(positions)), 
                frequency, 
                samples_per_segment, 
                max_error
            )
            while not self.service.startProfileCompletion().isDone():
                await asyncio.sleep(0.01)
            self.service.startProfileWait()
        except Exception as e:
            E_LOG(e)
