# coding: utf-8
"""Module to create a SIP package.

This module uses jinja2 templates in the ./package.j2 directory.
"""

import argparse
import os
from os.path import join
import logging

import jinja2



def create_package(package_path, package_title, overwrite=False):
    """Create a SIP package from the Jinja2 tempalte directory package.j2

    Parameters
    ----------
    package_path : str
        Path of the package to create with sip. eg.
        sip/execution_control/master_controller
    package_title : str
        Title of the Package. eg. Master Controller
    overwrite : bool
        If true, overwrite any exiting files in the package_path

    """
    logger = logging.getLogger()
    logger.info('Creating Package from template:')
    logger.info('- Path  : %s', package_path)
    logger.info('- Title : %s', package_title)
    loader = jinja2.FileSystemLoader(join(os.path.dirname(__file__), 'package.j2'))
    environment = jinja2.Environment(loader=loader)
    context = dict(title=package_title, description=r'\[Add Description!\]')
    for template in environment.list_templates(extensions='j2'):
        filepath, filename = os.path.split(template)
        template = environment.get_template(template)
        outpath = join(package_path, filepath, os.path.splitext(filename)[0])
        if not os.path.isdir(os.path.split(outpath)[0]):
            logger.debug('  - Creating directory : %s', os.path.split(outpath)[0])
            os.makedirs(os.path.split(outpath)[0])
        if not overwrite and os.path.isfile(outpath):
            logger.warning('    **WARNING** Ouput already exists, skipping. '
                           '[%s]', outpath)
            continue
        with open(outpath, 'w') as _file:
            logger.debug('    - Output   : %s', outpath)
            logger.debug('    - Template : %s', template.filename)
            _file.write(template.render(context))


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Create new SIP package')
    parser.add_argument('PATH', help="Package Path")
    parser.add_argument('TITLE', help="Package title")
    parser.add_argument('-o',
                        help="Over write any existing files in the specfied package "
                             "with those from the template directory (USE WITH CARE!)",
                        action='store_true')
    parser.add_argument('-v',
                        help="Verbose",
                        action='store_true')

    args = parser.parse_args()
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    if args.v:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    create_package(args.PATH, args.TITLE, args.o)

if __name__ == '__main__':
    main()
