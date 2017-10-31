# coding: utf-8
""" ZeroMQ based Logging aggregator service class.

This class implements a ZMQ SUB socket.

.. moduleauthor:: Ben Mort <benjamin.mort@oerc.ox.ac.uk>
"""
import json
import logging
import logging.handlers
import sys
import threading
import time

import zmq

from .logging_config import load_logging_config


class ZmqLoggingAggregator(threading.Thread):
    """ ZeroMQ logging aggregator service."""

    def __init__(self, config_file=None):
        """ Initialise"""
        threading.Thread.__init__(self)
        log_ = logging.getLogger('zla')

        # Define an event used to stop the thread.
        self._stop_requested = threading.Event()

        # Load the default logging configuration.
        if config_file:
            load_logging_config(config_file)
            log_.debug('Loaded config file: %s', config_file)

        # Create the ZMQ context and subscriber socket.
        log_.debug('Creating ZMQ Context')
        self.context = zmq.Context()
        log_.debug('Creating ZMQ SUB socket')
        self.subscriber = self.context.socket(zmq.SUB)

        # Bind the ZMQ subscriber socket.
        log_.debug('Binding to ZMQ SUB socket')
        self._connect()

    def stop(self):
        """ Stop the thread
        """
        self._stop_requested.set()

    def _connect(self, port=logging.handlers.DEFAULT_TCP_LOGGING_PORT):
        """Bind the subscriber socket to the specified port.

        Args:
            port (int): Subscriber port.
        """
        log_ = logging.getLogger('zla')
        try:
            self.subscriber.bind('tcp://*:{}'.format(port))
            self.subscriber.setsockopt_string(zmq.SUBSCRIBE, '')
        except zmq.ZMQError as error:
            log_.fatal('Failed to connect to ZMQ subscriber socket: %s',
                       error.strerror)
            sys.exit(error.errno)

    @staticmethod
    def _linspace(start, stop, number):
        """ Generates number values between start and stop.
        """
        if number == 1:
            yield stop
            return
        inc = (stop - start) / (number - 1)
        for i in range(number):
            yield start + inc * i

    def run(self):
        """ Logging aggregator event loop.

        Polls for new log messages on the ZMQ sub socket.
        """
        log_ = logging.getLogger('zla')
        log_.info('Started SIP ZMQ Logging aggregator')
        log = logging.getLogger('sip')

        # Exponential relaxation of the timeout in the event loop.
        fail_count = 0
        fail_count_limit = 50
        timeout = [10**exp for exp in self._linspace(-4, -1, fail_count_limit)]
        message_count = 0
        time_of_first_message = time.time()
        time_of_last_message = time.time()

        while not self._stop_requested.is_set():

            # Try to receive and display the log message.
            try:
                topic, values = self.subscriber.recv_multipart(zmq.NOBLOCK)
                str_values = values.decode('utf-8')
                try:
                    dict_values = json.loads(str_values)
                    dict_values['args'] = tuple(dict_values['args'])
                    record = logging.makeLogRecord(dict_values)
                    fail_count = 0
                    if message_count == 0:
                        time_of_first_message = time.time()
                        log_.debug('Message timer reset!')
                    message_count += 1
                    time_of_last_message = time.time()
                    log.handle(record)
                except json.decoder.JSONDecodeError:
                    log_.error('Unable to decode JSON log record.')
                    raise
            except zmq.ZMQError as error:
                if error.errno == zmq.EAGAIN:
                    fail_count += 1
                else:
                    raise  # Re-raise the exception

            # Set the timeout.
            if fail_count < fail_count_limit:
                _timeout = timeout[fail_count]
            else:
                _timeout = timeout[-1]

            if fail_count == fail_count_limit:
                log_.debug('Reached polling limit of {:.2f}s, '
                           '({} messages received in {:.2f}s)'
                           .format(_timeout, message_count,
                                   (time_of_last_message -
                                    time_of_first_message)))
                message_count = 0

            self._stop_requested.wait(_timeout)
