# -*- coding: utf-8 -*-
"""CLI to the Master Controller (RPyC flavour)"""
import logging
import argparse
import rpyc


class MasterControllerClient:
    def __init__(self, host, port):
        """Create a Master Controller client.

        Args:
            host (str): Master Controller RPyC Server host.
            port (int): Master Controller RPyC Server port.
        """
        logger = logging.getLogger('MasterControllerClient')
        try:
            self._connection = rpyc.connect(host, port)
        except ConnectionRefusedError as error:
            logger.critical('ERROR: Unable to connect!, %s', error.strerror)

    def command(self, command, *args):
        """Issue a command to the Master Controller."""
        commands = {
            'state': self.get_state,
            'health': self.get_health
        }
        commands[command](*args)

    def get_state(self):
        """Print the Master Controller state."""
        logger = logging.getLogger('MasterControllerClient')
        logger.info('State = %s', self._connection.root.get_state())

    def get_health(self):
        """Print the Master Controller health."""
        logger = logging.getLogger('MasterControllerClient')
        logger.info('Health = %s', self._connection.root.health_check())


def main():
    """Main function."""
    # Handle command line arguments
    parser = argparse.ArgumentParser(description='Master Controller CLI')
    parser.add_argument('--host', nargs=1, default='localhost', type=str,
                        help='Master Controller RPyC Server host '
                             '(default=localhost)')
    parser.add_argument('--port', nargs=1, default=12345, type=int,
                        help='Master Controller RPyC Server port '
                             '(default=12345)')
    parser.add_argument('COMMAND', choices=['state', 'health'],
                        help='Command to run.')
    parser.add_argument('ARGS', help='Command args.', nargs='*')

    args = parser.parse_args()

    client = MasterControllerClient(host=args.host, port=args.port)
    client.command(args.COMMAND, *args.ARGS)


if __name__ == '__main__':
    LOG = logging.getLogger()
    HANDLER = logging.StreamHandler()
    FORMAT_STR = "> [%(levelname).1s] %(message)-80s " \
                 "(%(name)s:L%(lineno)i) [%(asctime)s]"
    HANDLER.setFormatter(logging.Formatter(FORMAT_STR, '%H:%M:%S'))
    HANDLER.setLevel(logging.DEBUG)
    LOG.setLevel(logging.DEBUG)
    LOG.addHandler(HANDLER)
    main()
