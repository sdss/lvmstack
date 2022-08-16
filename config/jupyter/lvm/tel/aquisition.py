# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-08-18
# @Filename: lvm/tel/aquisition.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from cluplus.proxy import invoke, unpack, flatten
from lvmtipo.actors import lvm

# TODO: should go somewhere in a subclass
from logging import DEBUG, INFO
from sdsstools import get_logger

from astropy import units as u
from astropy.coordinates import SkyCoord, Angle

from lvmagp.focus import Focus
from .astrometry import Astrometry

import click


async def aquisition(telsubsys, ra:Angle, dec:Angle, exptime:float, level = INFO):
    try:
        # TODO: should go somewhere in a subclass
        logger = get_logger("lvm_tel_aquisition")
        logger.sh.setLevel(level)
        
        focus_temperature = 42 # TODO: get temperature from somewhere.
        
        focus = Focus(telsubsys)

        logger.debug(f"move tel/km {ra.hour}h:{dec.deg}d & temp2foc {focus_temperature}")

        await invoke(
            telsubsys.km.slewStart(ra.hour, dec.deg), 
            telsubsys.pwi.gotoRaDecJ2000(ra.hour, dec.deg),
            focus.nominal()
        )

        logger.debug(f"fake astrometry at radec {ra.hour}h:{dec.deg}d")

        ra_offset, dec_offset, focus_offset, km_offset = await Astrometry.calc(telsubsys, ra, dec, exptime)

        logger.debug(f"correct tel/km {ra_offset}:{dec_offset}/{km_offset} & focus offset {focus_offset}")

        await invoke( # there is no offsetting km
            telsubsys.pwi.offset(ra_add_arcsec = ra_offset, dec_add_arcsec = dec_offset),
            focus.offset(focus_offset)
        )

        logger.debug(f"done ")
        
    except Exception as ex:
        logger.error(ex)
        raise ex



@click.command()
@click.option('-v', '--verbose', count=True, help='Debug mode. Use additional v for more details.')
@click.option('-t', '--telsubsys', default='sci', help='Telescope subsystem: sci, skye, skyw or spec.')
@click.option('-e', '--exptime', default=5.0, help='Expose for for exptime seconds.')
@click.option('-r', '--ra', help='RA J2000.')
@click.option('-d', '--dec', help='DEC J2000.')
def main(verbose, telsubsys, exptime, ra, dec):
    import asyncio

    async def call(verbose, telsubsys, exptime, ra, dec):
        telsubsys = await lvm.from_string(telsubsys)
        await aquisition(telsubsys, Angle(ra), Angle(dec), exptime, level = DEBUG if args.verbose else INFO)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(call())

            
if __name__ == '__main__':

    main()


