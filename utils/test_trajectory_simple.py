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

def setSegment(km, idx, traj):
   t =  traj[idx]
   km.chat(1, 221, 4, 0, f"'{t[0]%cbuf} {t[1]} {t[2]} {t[3]} {t[4]} {t[5]}'")
   t =  traj[idx+1]
   km.chat(1, 221, 4, 0, f"'{t[0]%cbuf} 0 0 {t[3]} 0 0'")


def derot_now(traj):

    name="test.derot.km"
    amqpc = AMQPClient(name=f"{sys.argv[0]}.client-{uuid.uuid4().hex[:8]}")
    km = Proxy(amqpc, name).start()

    #km.chat(1,23,0)
    #json.loads(unpack(km.chat(1,1,0)))
    #km.chat(1,24,0)


    try:
       ## clear buffer
       km.chat(1, 226, 4)
    except:
        pass
    
    # create buffer
    km.chat(1, 220, 4, cbuf)

    km.moveAbsolute(traj[0][3])

    for i in range(4):
       setSegment(km, i, traj)

    # profile start from beginning
    km.chat(1, 222, 4, 0)

    upidx=4
    while upidx < len(traj)-1:
        try:
            moidx = int(json.loads(unpack(km.chat(1, 225, 4)))[-1].split(' ')[-1])
            updistance=((upidx%cbuf)-moidx+cbuf)%cbuf
            print(f"pos: {km.getPosition()} updist: {updistance} idx: {upidx}", end = '\r')
            if updistance < 4:
                setSegment(km,upidx,traj)
                upidx+=1
            sleep(0.2)
        
        except Exception as ex:
            print(ex)
            break


    ## profile stop
    km.chat(1, 224, 4)

    ## clear buffer
    km.chat(1, 226, 4)
    
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
        moc=sid.mpiaMocon(geoloc, point, None, deltaTime=args.deltaTime, polyN= int(args.polyN))
        derot_now(moc)
        
if __name__ == "__main__":
    main()
