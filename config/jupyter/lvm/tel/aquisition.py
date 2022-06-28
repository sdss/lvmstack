# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-08-18
# @Filename: lvm/tel/aquisition.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from lvmtipo.actors import lvm
from logging import DEBUG, INFO
from sdsstools import get_logger


from lvm.tel.focus import Focus
from lvm.tel.astrometry import Astrometry

import click

async def aquisition(telsubsys, ra, dec, exptime, fine_focus=False, logger = get_logger("lvm_tel_focus"), level = DEBUG):
    try:
        focus_temperature = 42 # get from somewhere a temperature.
        
        focus = Focus(telsubsys)

        logger.debug(f"move tel/km {ra}:{dec} & temp2foc {focus_temperature}")
        await invoke(
            telsubsys.km.slewStart(ra, dec), 
            telsubsys.pwi.gotoRaDecJ2000(ra, dec),
            focus.nominal(focus_temperature)
        )

        logger.debug(f"fake astrometry at radec {ra}:{dec}")

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
@click.option('-r', '--ra', type=float, help='RA J2000 in hours.')
@click.option('-d', '--dec', type=float, help='DEC J2000 in degrees.')
def main(verbose, telsubsys, exptime, ra, dec):

    loop=asyncio.get_event_loop()

    telsubsys = lvm.execute(lvm.from_string(telsubsys))

    lvm.execute(aquisition(telsubsys, ra, dec, exptime), verbose=verbose)

            
if __name__ == '__main__':

    main()


