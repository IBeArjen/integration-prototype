# -*- coding: utf-8 -*-
"""CLI to the Master Controller (REST flavour)"""
import logging
import argparse
import requests
import json


class MasterControllerClient:

    def __init__(self, host, port):
        """Create a Master Controller client.

        Args:
            host (str): Master Controller Server host.
            port (int): Master Controller Server port.
        """
        self._url = 'http://{}:{}'.format(host, port)

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
        if command == 'new_processing_block':
            if len(args) == 0:
                args = ['{}']
        commands[command](*args)

    def get_health(self):
        """Print the Master Controller health."""
        logger = logging.getLogger('MasterControllerClient')
        response = json.loads(requests.get(self._url + '/healthcheck'))
        logger.info('Response:', extra={'detail': response.text})

    def get_state(self):
        """Print the Master Controller state."""
        logger = logging.getLogger('MasterControllerClient')
        response = requests.get(self._url)
        logger.info('Response:', extra={'detail': response.text})

    def init(self):
        """Triggers the INIT state."""
        logger = logging.getLogger('MasterControllerClient')
        logger.info('Triggering the INIT state')
        response = requests.get(self._url + '/init')
        logger.info('Response:', extra={'detail': response.text})

    def standby(self):
        """Triggers the STANDBY state."""
        logger = logging.getLogger('MasterControllerClient')
        logger.info('Triggering the STANDBY state')
        response = requests.get(self._url + '/standby')
        logger.info('Response:', extra={'detail': response.text})

    def disable(self):
        """Triggers the DISABLE state."""
        logger = logging.getLogger('MasterControllerClient')
        logger.info('Triggering the DISABLE state')
        response = requests.get(self._url + '/disable')
        logger.info('Response:', extra={'detail': response.text})

    def online(self):
        """Triggers the ON state."""
        logger = logging.getLogger('MasterControllerClient')
        logger.info('Triggering the ON state')
        response = requests.get(self._url + '/on')
        logger.info('Response:', extra={'detail': response.text})

    def processing_blocks(self,):
        """Return a list of processing blocks."""
        logger = logging.getLogger('MasterControllerClient')
        block_info = requests.get(self._url + '/processing_blocks').text
        block_info = json.loads(block_info)
        logger.info('Block count = %i', block_info['count'])
        for block_id in block_info['block_ids']:
            logger.info('- %i', block_id)

    def new_processing_block(self, json_request):
        """Process processing block commands."""
        logger = logging.getLogger('MasterControllerClient')
        response = requests.post(self._url + '/processing_block/new',
                                 json=json.loads(json_request))
        logger.info('Created new processing block',
                    extra={'detail': response.text})

    def get_processing_block(self, identifier):
        """Get information on the processing block with the specified id."""
        logger = logging.getLogger('MasterControllerClient')
        response = requests.get(self._url +
                                '/processing_block/{}'.format(identifier))
        logger.info('Processing block info:', extra={'detail': response.text})

    def delete_processing_block(self, identifier):
        """Removes a processing block."""
        logger = logging.getLogger('MasterControllerClient')
        response = requests.get(self._url + '/processing_block/delete/{}'.
                                format(identifier))
        logger.info('Delete processing block:', extra={'detail': response.text})


def main():
    """Main function."""
    # Handle command line arguments
    parser = argparse.ArgumentParser(description='Master Controller CLI')
    parser.add_argument('--host', nargs='?', default='localhost', type=str,
                        help='Master Controller Server host '
                             '(default=localhost)')
    parser.add_argument('--port', nargs='?', default=5555, type=int,
                        help='Master Controller Server port '
                             '(default=5555)')
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


class CustomFilter(logging.Filter):
    def filter(self, record):
        if hasattr(record, 'detail') and len(record.detail) > 0:
            record.detail = '\n' + record.detail
        else:
            record.detail = ''
        return super(CustomFilter, self).filter(record)


if __name__ == '__main__':
    LOG = logging.getLogger('MasterControllerClient')
    HANDLER = logging.StreamHandler()
    FORMAT_STR = '> [%(levelname).1s] %(message)-80s ' \
                 '(%(name)s:L%(lineno)i) [%(asctime)s]%(detail)s'
    HANDLER.setFormatter(logging.Formatter(FORMAT_STR, '%H:%M:%S'))
    HANDLER.setLevel(logging.DEBUG)
    LOG.addFilter(CustomFilter())
    LOG.setLevel(logging.DEBUG)
    LOG.addHandler(HANDLER)
    main()
