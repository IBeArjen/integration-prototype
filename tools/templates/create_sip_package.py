# coding: utf-8
"""Module to create a SIP package.

This module uses jinja2 templates in the ./package.j2 directory.
"""

import argparse
import os
from os.path import join
import logging

import jinja2



def create_package(path, context, overwrite=False):
    """Create a SIP package from the Jinja2 tempalte directory package.j2

    Parameters
    ----------
    context : dict
        Jinja2 template context.
    overwrite : bool
        If true, overwrite any exiting files in the package_path

    """
    logger = logging.getLogger()
    logger.info('Creating Package from template:')
    logger.info('- Path  : %s', context['path'])
    logger.info('- Title : %s', context['title'])
    loader = jinja2.FileSystemLoader(join(os.path.dirname(__file__), 'package.j2'))
    environment = jinja2.Environment(loader=loader)
    if 'desc' not in context:
        context['desc'] = r'\[FIXME: Add better description!\]'
    if 'acronym' in context:
        context['acronym'] = '({})'.format(context['acronym'])
    for template in environment.list_templates(extensions='j2'):
        filepath, filename = os.path.split(template)
        template = environment.get_template(template)
        outpath = join(context['path'], filepath, os.path.splitext(filename)[0])
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
    context = dict(path=args.PATH, title=args.TITLE)
    create_package(context, args.o)

if __name__ == '__main__':
    main()
