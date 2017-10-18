# coding: utf-8
""" ZeroMQ logging aggregator service application

.. moduleauthor:: Ben Mort <benjamin.mort@oerc.ox.ac.uk>
"""
import logging
import logging.config
import os
import signal
import socket
import sys
import time

import bjoern
from bottle import Bottle, request, template

from .lib.zmq_logging_aggregator import ZmqLoggingAggregator

APP = Bottle()
START_TIME = time.time()


def signal_handler(signum, frame):
    """ Signal handler.

    Args:
        signum: Signal number received.
        frame: The current stack frame
    """
    # pylint: disable=unused-argument
    log = logging.getLogger(__name__)
    print(__name__)
    log.info('ZMQ Logging aggregator service received SIGINT')
    sys.exit(0)


@APP.route('/health')
def health_check():
    """ Health check HTTP endpoint
    """
    elapsed = time.time() - START_TIME
    return dict(module='zmq_logging_aggregator',
                hostname=socket.gethostname(),
                uptime=elapsed)


@APP.route('/my_ip')
def show_ip():
    """ Show IP address
    """
    ip = request.environ.get('REMOTE_ADDR')
    return template("Your IP is: {{ip}}", ip=ip)


def verify_config(config):
    """ Function to verity that the Logging Config sent to the logging
        configuration server is valid.
    """
    print(config)
    return config


def main():
    """ SIP ZMQ Logging aggregator service main.
    """
    log = logging.getLogger(__name__)
    signal.signal(signal.SIGINT, signal_handler)

    # Get path of config file.
    # TODO(BM) allow config to be set on command line?
    config_file = os.path.join(os.path.dirname(__file__),
                               'config', 'default.json')
    log.debug('Config file = %s', config_file)

    # Start logging aggregator thread.
    log.debug('Starting ZMQ logging aggregator')
    aggregator = ZmqLoggingAggregator(config_file)
    aggregator.daemon = True
    aggregator.start()

    # Start a logging configuration server.
    # https://docs.python.org/3.6/library/logging.config.html#logging.config.listen
    config_server = logging.config.listen(port=9999, verify=verify_config)
    config_server.daemon = True
    config_server.start()

    # Start the HTTP health check endpoint using bjoern
    bjoern.run(APP, host='0.0.0.0', port=5555)

    # Wait until the logging aggregator thread terminates.
    log.debug('Terminating logging aggregator service.')
    aggregator.join()

    log.debug('Terminating logging configuration server.')
    logging.config.stopListening()
    config_server.join()
