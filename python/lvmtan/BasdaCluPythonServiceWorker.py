# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-15
# @Filename: BasdaCluPythonServiceWorker.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


import sys
import time
import os

import asyncio
import logging

from functools import wraps

import click
from clu import AMQPActor, command_parser, Command
from clu.device import Device

from Nice import *
from Basda import *
from BasdaService import *

import numpy as np

actorServiceWorker = {}

class BasdaCluPythonServiceWorker(Worker):
   'python arpc worker'

   def __init__(self, _svcName):
      Worker.__init__(self, _svcName)
      self.counter = 0.0
      self.nodelist = []
      self.rootNode = Application.config()
      self.cfgDataNode = self.config("CFG.DATA")
      self.cfgNode = self.config("CFG")
      self.conn = {'name': self.name, 'user': 'guest', 'password': 'guest', 'host': '127.0.0.1', 'port': '5672', 'version': "0.1.0"}
      self.offline_wait = Time.seconds(1.0)
      self.online_wait = Time.seconds(0.1)
      self.loop = None;
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
        "additionalProperties": False
      }

    
   async def connect(self):
      await self.actor.start()
      return
      
   def wrapper(method):
        @wraps(method)
        def _impl(*method_args, **method_kwargs):
            cls = actorServiceWorker[method_args[0].actor.name]
            loop = cls.loop
            return asyncio.run_coroutine_threadsafe(method(cls, *method_args, **method_kwargs), cls.loop)
        return _impl  

   def init(self):
      if self.rootNode.exist("CLU.RABBITMQ.CONN") and self.rootNode.node("CLU.RABBITMQ.CONN").hasLeaf():
        self.conn.update(self.rootNode.node("CLU.RABBITMQ.CONN").MapStringString.toPy())
      if self.cfgNode.exist("RABBITMQ.CONN") and self.cfgNode.node("RABBITMQ.CONN").hasLeaf():
        self.conn.update(self.cfgNode.node("RABBITMQ.CONN").MapStringString.toPy())
        
      asyncio.set_event_loop(asyncio.new_event_loop())
   
      self.loop = asyncio.get_event_loop()
      self.actor = AMQPActor(
            name=self.conn["name"],
            user=self.conn["user"],
            password=self.conn["password"],
            host=self.conn["host"],
            port = int(self.conn["port"]),
            version=self.conn["version"],
#            loop=self.loop,
      )
      
      self.actor.load_schema(self.schema, is_file=False)
      
      actorServiceWorker[self.conn["name"]]=self
        
      if self.cfgNode.exist("OFFLINE_WAIT") and self.cfgNode.node("OFFLINE_WAIT").hasLeaf():
        self.offline_wait = self.cfgNode.node("OFFLINE_WAIT").Time
      if self.cfgNode.exist("ONLINE_WAIT") and self.cfgNode.node("ONLINE_WAIT").hasLeaf():
        self.online_wait = self.cfgNode.node("ONLINE_WAIT").Time

      if not self.service and self.cfgNode.exist("SERVICE") and self.cfgNode.node("SERVICE").hasLeaf():
        U9_LOG(self.cfgNode.node("SERVICE").String)
        self.service = Basdard.interface(self.cfgNode.node("SERVICE").String)


     
   def abort(self):
      self.terminated = True 
      U8_LOG("abort") 

   #def terminate(self):
      #self.terminated = True 
      #U8_LOG("terminate") 

   def deinit(self):
      #if  self.connection:
        #self.loop.run_until_complete(self.connection.close())
        self.loop.shutdown_asyncgens()
        self.loop.close()

   def activate(self):
      I_LOG("Connecting %s " % self.conn) 
      try:
        self.loop.run_until_complete(self.connect())
        N_LOG("Connected to %s " % self.conn) 
        return
    
      except ConnectionRefusedError as e:
        F_LOG(e)
        self.worker.setState(ServiceState.OFFLINE)

      except ConnectionError as e:
        F_LOG(e)
        self.worker.setState(ServiceState.OFFLINE)
        
      except Exception as e:
        F_LOG(e)
        self.worker.setState(ServiceState.OFFLINE)

      N_LOG("Failed connecting %s " % self.conn) 
        

   def idleOffline(self):
      if not self.worker.timedWaitForNewState(self.offline_wait):
        self.worker.setState(ServiceState.ONLINE)

   def idleOnline(self):
      while not self.worker.timedWaitForNewState(Time.seconds(0.01)):
        tasks = asyncio.Task.all_tasks(self.loop)
        if len(tasks):
           self.loop.run_until_complete(asyncio.wait(tasks, timeout=0.1))
      #if not self.worker.timedWaitForNewState(self.online_wait):
        #self.worker.setState(ServiceState.WORKING)

   async def runWhileStateIsWORKING(self):
       return

   #def work(self):
      #U9_LOG("Work %s" % self.worker.state())
#          self.loop.run_forever()
       

