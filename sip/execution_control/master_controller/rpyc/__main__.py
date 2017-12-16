# -*- coding: utf-8 -*-
"""SDP Element Master (RPyC flavour).

.. moduleauthor:: Benjamin Mort <benjamin.mort@oerc.ox.ac.uk>
"""

import logging
import random
import socket
from time import time

import rpyc
from rpyc.utils.server import ThreadedServer

START_TIME = time()


class MasterControllerService(rpyc.Service):
    """RPyC service for the Master Controller."""

    def __init__(self, *args):
        """Constructor."""
        super().__init__(*args)
        self.logger = logging.getLogger('MasterController')

    def on_connect(self):
        """Called when connection is established."""
        print('Connected!')

    def on_disconnect(self):
        """Called after service disconnects (for cleanup)"""
        print('Disconnected!')

    @staticmethod
    def exposed_health_check():
        """Return a health check message."""
        return dict(module='Master Controller',
                    hostname=socket.gethostname(),
                    uptime=time() - START_TIME)

    @staticmethod
    def exposed_get_state():
        """Return the SDP state."""
        states = ['OFF', 'INIT', 'STANDBY', 'ON', 'DISABLE', 'FAULT', 'ALARM',
                  'UNKNOWN']
        return random.choice(states)


def main():
    """Master Controller main function."""
    server = ThreadedServer(MasterControllerService, port=12345)
    server.start()


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


