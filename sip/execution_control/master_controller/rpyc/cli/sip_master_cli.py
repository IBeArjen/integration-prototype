# -*- coding: utf-8 -*-
"""CLI to the Master Controller (RPyC flavour)"""
import argparse
import logging

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
        logger = logging.getLogger('MasterControllerClient')
        commands = {
            'health': self.get_health,
            'state': self.get_state,
            'init': self.init,
            'standby': self.standby,
            'disable': self.disable,
            'online': self.online,
            'processing_blocks': self.processing_blocks,
            'new_processing_block': self.new_processing_block,
            'processing_block': self.get_processing_block,
            'delete_processing_block': self.delete_processing_block
        }
        if command not in commands:
            logger.error('Command "%s" not registered with the CLI.',
                         command)
            return None
        commands[command](*args)

    def get_health(self):
        """Print the Master Controller health."""
        logger = logging.getLogger('MasterControllerClient')
        logger.info('Health = %s', self._connection.root.health_check())

    def get_state(self):
        """Print the Master Controller state."""
        logger = logging.getLogger('MasterControllerClient')
        logger.info('State = %s', self._connection.root.get_state())

    def init(self):
        """Triggers the INIT state."""
        logger = logging.getLogger('MasterControllerClient')
        logger.info('Setting INIT state.')
        self._connection.root.init()

    def standby(self):
        """Triggers the STANDBY state."""
        logger = logging.getLogger('MasterControllerClient')
        logger.info('Setting STANDBY state.')
        self._connection.root.standby()

    def disable(self):
        """Triggers the DISABLE state."""
        logger = logging.getLogger('MasterControllerClient')
        logger.info('Setting DISABLE state.')
        self._connection.root.disable()

    def online(self):
        """Triggers the ONLINE state."""
        logger = logging.getLogger('MasterControllerClient')
        logger.info('Setting ONLINE state.')
        self._connection.root.online()

    def processing_blocks(self,):
        """Return a lit of proccessing blocks."""
        logger = logging.getLogger('MasterControllerClient')
        block_info = self._connection.root.processing_blocks()
        logger.info('Block count = %i', block_info['count'])
        for block_id in block_info['block_ids']:
            logger.info('- %i', block_id)

    def new_processing_block(self, json_request):
        """Process processing block commands."""
        logger = logging.getLogger('MasterControllerClient')
        logger.info('Requesting new processing block')
        response = self._connection.root.new_processing_block(json_request)
        if 'id' in response:
            logger.info('Processing block created with id = %i',
                        response['id'])
        else:
            logger.error('Failed to create processing block.')

    def get_processing_block(self, identifier):
        """Get information on the processing block with the specified id."""
        logger = logging.getLogger('MasterControllerClient')
        response = self._connection.root.processing_block(identifier)
        if 'id' in response:
            logger.info(response)
        else:
            logger.error(response)

    def delete_processing_block(self, identifier):
        """Removes a processing block."""
        logger = logging.getLogger('MasterControllerClient')
        reponse = self._connection.root.delete_processing_block(identifier)
        if 'id' in reponse:
            logger.info(reponse)
        else:
            logger.error(reponse)


def main():
    """Main function."""
    # Handle command line arguments
    parser = argparse.ArgumentParser(description='Master Controller CLI')
    parser.add_argument('--host', nargs='?', default='localhost', type=str,
                        help='Master Controller RPyC Server host '
                             '(default=localhost)')
    parser.add_argument('--port', nargs='?', default=12345, type=int,
                        help='Master Controller RPyC Server port '
                             '(default=12345)')
    parser.add_argument('COMMAND', choices=['state',
                                            'health',
                                            'init',
                                            'standby',
                                            'disable',
                                            'online',
                                            'processing_blocks',
                                            'new_processing_block',
                                            'processing_block',
                                            'delete_processing_block'],
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
