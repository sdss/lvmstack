#!/usr/bin/bash

import sys
import uuid
from logging import DEBUG
from time import sleep

from clu import AMQPClient, CommandStatus

from cluplus.proxy import Proxy, invoke, unpack

import json

from clu import AMQPClient, CommandStatus

from cluplus.proxy import Proxy, invoke, unpack

cbuf = 20
module = 4
dist = 7

name="test.derot.km"
amqpc = AMQPClient(name=f"{sys.argv[0]}.client-{uuid.uuid4().hex[:8]}")
#amqpc.log.sh.setLevel(DEBUG)

km = Proxy(amqpc, name).start()


def setSegment(km, idx, t0, t1=None):
   print (f"'{idx%cbuf} {t0[0]} {t0[1]} {t0[2]} {t0[3]} {t0[4]}'")
   km.chat(1, 221, module, 0, f"'{idx%cbuf} {t0[0]} {t0[1]} {t0[2]} {t0[3]} {t0[4]}'")
   if t1:
       print(f"'{(idx+1)%cbuf} 0 0 {t1[2]} 0 0'")
       km.chat(1, 221, module, 0, f"'{(idx+1)%cbuf} 0 0 {t1[2]} 0 0'")


def derot_now(sid, geoloc, point, deltaTime, polyN):

    traj = sid.mpiaMocon(geoloc, point, None, deltaTime=deltaTime, polyN=1)

    if traj[0][3] < 0:
        print(traj)
        print(f"Error position {traj[0][3]} < 0")
        return
    
    if polyN < dist:
        print(f"Minimum {dist} segments")
    
    km.moveAbsolute(traj[0][3]-1000)

    #km.chat(1,23,0)
    #json.loads(unpack(km.chat(1,1,0)))
    #km.chat(1,2module,0)
 
    try:
       ## clear buffer
       km.chat(1, 226, module)
    except:
        pass
    
    # create buffer
    km.chat(1, 220, module, cbuf)

    now = astropy.time.Time.now()
    print(now)
    traj = sid.mpiaMocon(geoloc, point, None, deltaTime=deltaTime, polyN=dist, time=now)

    km.moveAbsolute(traj[0][3])

    for i in range(dist):
       setSegment(km, i, traj[i])
    setSegment(km, i+1, traj[i+1])

    # profile start from beginning
    km.chat(1, 222, module, 0)

    upidx=dist
    while upidx < polyN:
        try:
            moidx = int(json.loads(unpack(km.chat(1, 225, module)))[-1].split(' ')[-1])
            updistance=((upidx%cbuf)-moidx+cbuf)%cbuf
            print(f"pos: {km.getIncrementalEncoderPosition()} {km.getDeviceEncoderPosition()} updist: {updistance} idx: {upidx}", end = '\n')
            if updistance < dist:
                nowpdt = now + astropy.time.TimeDelta(deltaTime*upidx, format='sec')
                print(nowpdt)
                sid.mpiaMocon(geoloc, point, None, deltaTime=deltaTime, polyN=1, time=nowpdt)
                setSegment(km, upidx, traj[0], traj[1])
                upidx+=1
            sleep(0.2)
        
        except Exception as ex:
            print(ex)
            break


    ## profile stop
    km.chat(1, 224, module)

    ## clear buffer
    km.chat(1, 226, module)
    
    print("done")


import math
import numpy
import astropy.coordinates
import astropy.time
import astropy.units

from lvmtipo.site import Site
from lvmtipo.siderostat import Siderostat
from lvmtipo.fiber import Fiber
from lvmtipo.target import Target


def main():
    """ Example application demonstrating the interface.
    Examples:
    ./test_trajectory_simple -r 230 -d -80 -f P2-2
    ./test_trajectory_simple.py -r 230 -d -80 -N 10
    .. todo demonstrate use of proper motions 
    """
    import argparse
    parser = argparse.ArgumentParser()
    # parser.add_argument("-v", '--verbose', action='store_true',
    #                     help="print some notes to stdout")

    # right ascension in degrees
    parser.add_argument("-r", '--ra', help="RA J2000 in degrees or in xxhxxmxxs format")

    # declination in degrees
    parser.add_argument("-d", '--dec', help="DEC J2000 in degrees or in +-xxdxxmxxs format")

    # shortcut for site coordinates: observatory
    parser.add_argument("-s", '--site', default="LCO", help="LCO or MPIA or APO or KHU")

    # optional
    parser.add_argument("-T", '--deltaTime', type=int, default=1, help="time covered by a single polynomial in seconds")

    # optional number of mocon polynomials
    parser.add_argument("-N", '--polyN', help="number of mocon polynomials")

    args = parser.parse_args()

    # check ranges and combine ra/dec into a astropy SkyCoord
    if args.ra is not None and args.dec is not None :
        if args.ra.find("h") < 0 :
            # apparently simple floating point representation
            targ = astropy.coordinates.SkyCoord(ra=float(args.ra), dec=float(args.dec),unit="deg")
        else :
            targ = astropy.coordinates.SkyCoord(args.ra + " " + args.dec)
    else :
        targ = None

    # step 1: define where the observatory is on Earth
    geoloc = Site(name = args.site)
    # print(geoloc)

    # step 2: define where the output beam of the siderostat points to
    # and use the LCO defaults.
    sid = Siderostat()
    # print(sid)

    # step 3: define where the sidereostat is pointing on the sky
    point = Target(targ)
    print("target is ",targ)

    # calculate the field angle (in radians)
    rads = sid.fieldAngle(geoloc, point, None)
    print("field angle " + str(math.degrees(rads)) + " deg")

    # If the command line option -N was used, construct
    # the mocon external profile data as a list of lists:
    if args.polyN is not None :
        derot_now(sid, geoloc, point, int(args.deltaTime), int(args.polyN))
        
if __name__ == "__main__":
    main()
