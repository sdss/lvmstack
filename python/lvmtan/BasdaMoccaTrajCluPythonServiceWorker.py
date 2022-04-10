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

from Nice import I_LOG, U9_LOG
from .BasdaMoccaXCluPythonServiceWorker import *

import asyncio
import math
import numpy
import astropy.coordinates
import astropy.time
import astropy.units as u

from lvmtipo.site import Site
from lvmtipo.siderostat import Siderostat
from lvmtipo.fiber import Fiber
from lvmtipo.target import Target

from astropy.utils import iers
iers.conf.auto_download = False

class BasdaMoccaTrajCluPythonServiceWorker(BasdaMoccaXCluPythonServiceWorker):
    "python clu worker"

    def __init__(self, _svcName):
        BasdaMoccaXCluPythonServiceWorker.__init__(self, _svcName)
        self.task = None
        self.geoloc = None
        self.sid = Siderostat()
        self.point = None

    def _status(self, reachable=True):
        return {**BasdaMoccaXCluPythonServiceWorker._status(self), **{"CurrentTime": self.service.getCurrentTime() if reachable else "Unknown"}}

    async def slewTick(self, delta_time):
        while True:
            try:
               position = math.degrees(self.sid.fieldAngle(self.geoloc, self.point, None))
#               U9_LOG(f"field angle {position} deg")
               self.service.moveAbsolute(position, "DEG")
            except Exception as e:
                command.fail(error=e)

            await asyncio.sleep(delta_time)


    @command_parser.command("slewStart")
    @click.argument("RA", type=float)
    @click.argument("DEC", type=float)
    @click.argument("DELTA_TIME", type=int, default=1)
    @click.argument("SITE", type=str, default="LCO")
    @BasdaCluPythonServiceWorker.wrapper
    async def slewStart(
        self,
        command: Command,
        ra: float,
        dec: float,
        delta_time: int,
        site: str,
    ):
        """Start slew"""
        I_LOG(f"start slew now {ra} {dec} {delta_time} {site}")

        targ = astropy.coordinates.SkyCoord(ra=ra, dec=dec, unit=(u.hourangle, u.deg))
#        I_LOG(astropy.version.version)

        self.point = Target(targ)

        self.geoloc = Site(name = site)

        # calculate the field angle (in radians)
        try:
            position = math.degrees(self.sid.fieldAngle(self.geoloc, self.point, None))
            
            I_LOG(f"field angle {position} deg")
            self.service.moveAbsoluteStart(position, "DEG")
            while not self.service.moveAbsoluteCompletion().isDone():
                await asyncio.sleep(0.1)
                command.info(
                    Position=self.service.getPosition(),
                    DeviceEncoder={"Position": self.service.getDeviceEncoderPosition("STEPS"), "Unit": "STEPS"},
                    Velocity=self.service.getVelocity(),
                    AtHome=self.service.isAtHome(),
                    AtLimit=self.service.isAtLimit(),
                )
            self.service.moveAbsoluteWait()

        except Exception as e:
            return command.fail(error=e)

        try:
            loop = asyncio.get_event_loop()
            if self.task:
                self.task.cancel()
            self.task = loop.create_task(self.slewTick(delta_time))
        except Exception as e:
            command.fail(error=e)

        return command.finish(**self._status())
            
            

    @command_parser.command("slewStop")
    @BasdaCluPythonServiceWorker.wrapper
    async def slewStop(
        self,
        command: Command
    ):
        """Stop slew"""
        if self.task:
            self.task.cancel()
            self.task = None

        return command.finish(**self._status())
        
    

    #@command_parser.command("changeProfile")
    #@click.argument("START_DATE", type=datetime.datetime)
    ##   @click.argument('POSITIONS', cls=ConvertStrToList, type=list)
    #@click.argument("POSITIONS", type=list)
    #@BasdaCluPythonServiceWorker.wrapper
    #async def changeProfile(self, start_date: datetime.datetime, positions: list):
        #"""Change active trajectory"""
        ## U8_LOG("changeProfile %s %s %s" % (start_date, positions, type(self.service)))
        #try:
            #self.service.changeProfile(Nice.Date.now(), Nice.NPoint(Nice.NPoint(positions)))
        #except Exception as e:
            #command.fail(error=e)

    #@command_parser.command("startProfile")
    #@click.argument("START_DATE", type=datetime.datetime)
    #@click.argument("POSITIONS", type=list)
    #@click.argument("FREQUENCY", type=int)
    #@click.argument("SAMPLES_PER_SEGMENT", type=int)
    #@click.argument("MAX_ERROR", type=int)
    #@BasdaCluPythonServiceWorker.wrapper
    #async def startProfile(
        #self,
        #start_date: datetime.datetime,
        #positions: list,
        #frequency: int,
        #samples_per_segment: int,
        #max_error: int,
    #):
        #"""Start trajectory"""
        ## U8_LOG("startProfile %s %s %s %s %s" % (start_date, positions, frequency, samples_per_segment, max_error))
        #try:
            #self.service.startProfileStart(
                #Nice.Date.fromUTC(
                    #start_date.year,
                    #start_date.month,
                    #start_date.day,
                    #start_date.hour,
                    #start_date.minute,
                    #start_date.second,
                    #start_date.microsecond * 1000,
                #),
                #Nice.NPoint(Nice.NPoint(positions)),
                #frequency,
                #samples_per_segment,
                #max_error,
            #)
            #while not self.service.startProfileCompletion().isDone():
                #await asyncio.sleep(0.01)
            #self.service.startProfileWait()
        #except Exception as e:
            #command.fail(error=e)
