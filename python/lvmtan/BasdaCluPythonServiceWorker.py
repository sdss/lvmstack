# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-15
# @Filename: BasdaCluPythonServiceWorker.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


import asyncio
import logging
import os
import sys
import time
from functools import wraps

import click
import numpy as np
import Nice
import Basda 
import BasdaService

from clu import AMQPActor, Command, command_parser
from clu.device import Device
from . import __version__

actorServiceWorker = {}


class BasdaCluPythonServiceWorker(BasdaService.Worker):
    "python arpc worker"

    def __init__(self, _svcName):
        BasdaService.Worker.__init__(self, _svcName)
        self.counter = 0.0
        self.nodelist = []
        self.rootNode = Nice.Application.config()
        self.cfgDataNode = self.config("CFG.DATA")
        self.cfgNode = self.config("CFG")
        self.conn = {
            "name": self.name,
            "user": "guest",
            "password": "guest",
            "host": "127.0.0.1",
            "port": "5672",
            "version": __version__,
        }
        self.offline_wait = Nice.Time.seconds(1.0)
        self.online_wait = Nice.Time.seconds(0.1)
        self.loop = None
        self.actor = None
        self.svc = None
        self.service = None
        self.terminated = False
        self.schema = {
            "type": "object",
            "properties": {
                "State": {"type": "string"},
                "Units": {"type": "string"},
            },
            "additionalProperties": False,
        }

    async def connect(self):
        await self.actor.start()
        return

    def wrapper(method):
        @wraps(method)
        def _impl(*method_args, **method_kwargs):
            cls = actorServiceWorker[method_args[0].actor.name]
            loop = cls.loop
            return asyncio.run_coroutine_threadsafe(
                method(cls, *method_args, **method_kwargs), cls.loop
            )

        return _impl

    def init(self):
        if (
            self.rootNode.exist("CLU.RABBITMQ.CONN")
            and self.rootNode.node("CLU.RABBITMQ.CONN").hasLeaf()
        ):
            self.conn.update(
                self.rootNode.node("CLU.RABBITMQ.CONN").MapStringString.toPy()
            )
        if (
            self.cfgNode.exist("RABBITMQ.CONN")
            and self.cfgNode.node("RABBITMQ.CONN").hasLeaf()
        ):
            self.conn.update(self.cfgNode.node("RABBITMQ.CONN").MapStringString.toPy())

        asyncio.set_event_loop(asyncio.new_event_loop())

        self.loop = asyncio.get_event_loop()
        self.actor = AMQPActor(
            name=self.conn["name"],
            user=self.conn["user"],
            password=self.conn["password"],
            host=self.conn["host"],
            port=int(self.conn["port"]),
            version=self.conn["version"],
            #            loop=self.loop,
        )

        self.actor.load_schema(self.schema, is_file=False)

        actorServiceWorker[self.conn["name"]] = self

        if (
            self.cfgNode.exist("OFFLINE_WAIT")
            and self.cfgNode.node("OFFLINE_WAIT").hasLeaf()
        ):
            self.offline_wait = self.cfgNode.node("OFFLINE_WAIT").Time
        if (
            self.cfgNode.exist("ONLINE_WAIT")
            and self.cfgNode.node("ONLINE_WAIT").hasLeaf()
        ):
            self.online_wait = self.cfgNode.node("ONLINE_WAIT").Time

        if (
            not self.service
            and self.cfgNode.exist("SERVICE")
            and self.cfgNode.node("SERVICE").hasLeaf()
        ):
            Nice.U9_LOG(self.cfgNode.node("SERVICE").String)
            self.service = Basda.Basdard.interface(self.cfgNode.node("SERVICE").String)

    def abort(self):
        self.terminated = True
        Nice.U8_LOG("abort")

    # def terminate(self):
    # self.terminated = True
    # Nice.U8_LOG("terminate")

    def deinit(self):
        # if  self.connection:
        # self.loop.run_until_complete(self.connection.close())
        self.loop.shutdown_asyncgens()
        self.loop.close()

    def activate(self):
        Nice.I_LOG("Connecting %s " % self.conn)
        try:
            self.loop.run_until_complete(self.connect())
            Nice.N_LOG("Connected to %s " % self.conn)
            return

        except ConnectionRefusedError as e:
            Nice.F_LOG(e)
            self.worker.setState(BasdaService.ServiceState.OFFLINE)

        except ConnectionError as e:
            Nice.F_LOG(e)
            self.worker.setState(BasdaService.ServiceState.OFFLINE)

        except Nice.Exception as e:
            Nice.F_LOG(e)
            self.worker.setState(BasdaService.ServiceState.OFFLINE)

        Nice.N_LOG("Failed connecting %s " % self.conn)

    def idleOffline(self):
        if not self.worker.timedWaitForNewState(self.offline_wait):
            self.worker.setState(BasdaService.ServiceState.ONLINE)

    def idleOnline(self):
        while not self.worker.timedWaitForNewState(Nice.Time.seconds(0.01)):
            tasks = asyncio.Task.all_tasks(self.loop)
            self.loop.run_until_complete(asyncio.gather(*tasks))

    async def runWhileStateIsWORKING(self):
        return
