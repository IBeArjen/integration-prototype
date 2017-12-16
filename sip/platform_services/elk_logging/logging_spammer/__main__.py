# coding: utf-8
"""Dummy app to spam a bunch of logs"""
import time
import random
import socket
import sys
import logging

import logstash


def hostname_resolves(hostname):
    """Return True if the host name can be resolved, otherwise False."""
    try:
        socket.gethostbyname(hostname)
        return True
    except socket.error:
        return False


def main():
    """Main Program"""
    log = logging.getLogger('logging_spammer')
    log.setLevel(logging.DEBUG)

    host_name = socket.gethostname()
    address = socket.gethostbyname(host_name)
    print('hostname = {}, address = {}'.format(host_name, address))

    # For the host to be resolved the container must be in the same overlay
    # network as the logstash container.
    host = 'logstash'
    if hostname_resolves(host):
        handler = logstash.LogstashHandler(host, port=5000, version=1)
        log.addHandler(handler)
    else:
        handler = logging.StreamHandler(stream=sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        log.addHandler(handler)

    levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR,
              logging.CRITICAL]
    start_time = time.time()
    try:
        while True:
            elapsed = time.time() - start_time
            log.log(random.choice(levels),
                    'hello from %s (%.1f s)', host_name, elapsed)
            time.sleep(random.uniform(0.01, 0.5))
    except KeyboardInterrupt:
        print('Exiting...')


if __name__ == '__main__':
    main()
