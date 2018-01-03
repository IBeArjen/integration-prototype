# -*- coding: utf-8 -*-
"""SDP Element Master (REST flavour).

Run with:
    python3 -m bottle --server bjoern --bind 0.0.0.0:5555 \
        sip.execution_control.master_controller.rest.__main__:APP
or:
    python3 -m sip.execution_control.master_controller.rest

.. moduleauthor:: Benjamin Mort <benjamin.mort@oerc.ox.ac.uk>
"""

import logging
import random
import socket
from time import time

import bjoern
from bottle import Bottle, request, HTTPResponse


APP = Bottle()
START_TIME = time()


@APP.get('/healthcheck')
def health_check():
    """Health check endpoint."""
    return dict(module='Master Controller',
                hostname=socket.gethostname(), uptime=time() - START_TIME)


@APP.get('/')
@APP.get('/state')
def get_state():
    """Get the SDP state."""
    states = ['OFF', 'INIT', 'STANDBY', 'ON', 'DISABLE', 'FAULT', 'ALARM',
              'UNKNOWN']
    return dict(module='Master Controller', state=random.choice(states))


@APP.get('/set_state/<state>')
def set_state(state):
    """Set the SDP state."""
    assert state.isalpha()
    state = state.upper()
    states = ['OFF', 'INIT', 'STANDBY', 'ON', 'DISABLE', 'FAULT', 'ALARM',
              'UNKNOWN']
    if state not in states:
        return HTTPResponse(status=300, body=dict(error='Invalid state.',
                                                  allowed_states=states))
    return dict(module='Master Controller',
                message='Setting state to {}'.format(state))


@APP.get('/processing_blocks')
def processing_blocks():
    """Returns a list of processing blocks."""
    block_ids = [random.randrange(0, 100)
                 for _ in range(random.randint(0, 10))]
    return dict(count=len(block_ids), block_ids=sorted(block_ids))


@APP.post('/processing_block/new')
def new_processing_block():
    """Creates a new processing block."""
    request_data = request.json
    return dict(id=random.randint(0, 1000), request=request_data)


@APP.get('/processing_block/<identifier:int>')
def get_processing_block(identifier):
    """Returns information on a processing block."""
    if random.choice([True, False]):
        return HTTPResponse(status=300,
                            body=dict(error='Unknown processing block'))
    states = ['INIT', 'RUNNING', 'FINISHED']
    return dict(id=identifier, state=random.choice(states))


@APP.get('/processing_block/delete/<identifier:int>')
@APP.get('/processing_block/rm/<identifier:int>')
def delete_processing_block(identifier):
    """Removes a processing block."""
    if random.choice([True, False]):
        return HTTPResponse(status=300,
                            body=dict(error='Unknown processing block'))
    return dict(message='Removed processing block', id=identifier)


@APP.post('/capacity')
def set_state():
    """Returns current capacity to engage resources in processing.

    Takes JSON input with fields:

    - type (str): The processing type
    - baselines (int): Number of baselines / beams
    - frequencies (int): Frequency band extent

    Returns a JSON string with:

    - ingest buffer availability for the processing specified as available
      ingest time in seconds.

    Test with:
        curl -H "Content-Type: application/json" -X POST \
            -d '{"type":"ical", "baselines":20}' \
            http://localhost:5555/capacity
    """
    request_data = request.json
    if 'type' not in request_data:
        return HTTPResponse(status=300,
                            body=dict(error='Invalid or unspecified type'))
    return dict(request=request_data,
                ingest_time=random.randint(0, 3600 * 20))


def main():
    """Master Controller main function."""
    logger = logging.getLogger('MasterController')
    try:
        # Bind to TCP host/port (0.0.0.0 == bind to all IPv4 address)
        bjoern.run(APP, host='0.0.0.0', port=5555)
    except OSError as error:
        logger.critical("ERROR: Unable to start health check API: %s",
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


