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

    states = ['OFF', 'INIT', 'STANDBY', 'ON', 'DISABLE', 'FAULT', 'ALARM',
              'UNKNOWN']

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

    def exposed_get_state(self):
        """Return the SDP state."""
        return random.choice(self.states)

    def exposed_set_state(self, state):
        """Sets the SDP state.

        Args:
            state (str): The state to set.

        Returns:
            (bool) True if successful, otherwise False.
        """
        if state not in self.states:
            return False
        else:
            return True

    @staticmethod
    def exposed_processing_blocks():
        """Return a list of processing blocks."""
        block_ids = [random.randrange(0, 100)
                     for _ in range(random.randint(0, 10))]
        return dict(count=len(block_ids), block_ids=sorted(block_ids))

    @staticmethod
    def exposed_new_processing_block(request):
        """Creates a new processing block matching the specified request

        Args:
            request (str): JSON string with the processing block request.

        Returns:
            (dict) Request response
        """
        if random.choice([True, False]):
            return dict(id=random.randint(0, 1000),
                        request=request)
        else:
            return dict(error='Unable to create processing block.',
                        request=request)

    @staticmethod
    def exposed_processing_block(identifier):
        """Returns information on a processing block."""
        if random.choice([True, False]):
            return dict(error='Unable to find processing block')
        else:
            states = ['INIT', 'RUNNING', 'FINISHED']
            return dict(id=identifier, state=random.choice(states))

    @staticmethod
    def exposed_delete_processing_block(identifier):
        """Removes a processing block."""
        if random.choice([True, False]):
            return dict(error='Unable to find processing block')
        else:
            return dict(id=identifier, message='Removed processing block.')


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


