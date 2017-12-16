# -*- coding: utf-8 -*-
"""SDP Element Master (REST flavour).

.. moduleauthor:: Benjamin Mort <benjamin.mort@oerc.ox.ac.uk>
"""

import logging
import random
import socket
from time import time

import bjoern
from bottle import Bottle

APP = Bottle()
START_TIME = time()


@APP.route('/healthcheck')
def health_check():
    """Health check endpoint."""
    return dict(module='Master Controller',
                hostname=socket.gethostname(),
                uptime=time() - START_TIME)


@APP.route('/')
@APP.route('/state')
def get_state():
    """Get the SDP state."""
    states = ['OFF', 'INIT', 'STANDBY', 'ON', 'DISABLE', 'FAULT', 'ALARM',
              'UNKNOWN']
    return dict(module='Master Controller',
                state=random.choice(states))


def main():
    """Master Controller main function."""
    logger = logging.getLogger('MasterController')
    try:
        # Bind to TCP host/port (0.0.0.0 == bind to all IPv4 address)
        bjoern.run(APP, host='0.0.0.0', port=5555)
    except OSError as error:
        logger.critical("ERROR: Unable to start healthcheck API: %s",
                        error.strerror)
    except KeyboardInterrupt:
        logger.info('Terminated Master Controller!')


if __name__ == "__main__":
    LOG = logging.getLogger()
    HANDLER = logging.StreamHandler()
    FORMAT_STR = "> [%(levelname).1s] %(message)-80s " \
                 "(%(name)s:L%(lineno)i) [%(asctime)s]"
    HANDLER.setFormatter(logging.Formatter(FORMAT_STR, '%H:%M:%S'))
    HANDLER.setLevel(logging.DEBUG)
    LOG.setLevel(logging.DEBUG)
    LOG.addHandler(HANDLER)
    main()


