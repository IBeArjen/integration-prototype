# -*- coding: utf-8 -*-
"""Script to create initial set of SIP packages.

Usage:

    python3 tools/templates/create_initial_packages.py [options]

"""
import argparse
import shutil
import os
from os.path import join, dirname, split, splitext, isfile, isdir
import json
import logging

import jinja2
import yaml


def create_package(path, context, overwrite=False, add_tests=True,
                   dry_run=False):
    """Create a SIP package from the Jinja2 template directory package.j2

    Parameters
    ----------
    path : str
        Path of the package to create.
    context : dict
        Jinja2 template context dictionary containing template replacements.
    overwrite : bool, optional
        If True, overwrite any exiting files in the package_path
    add_tests : bool, optional
        If True, add a tests directory to the package
    dry_run : bool, optional
        If True, don't actually create directories
    """
    logger = logging.getLogger()
    if dry_run:
        logger.setLevel(logging.DEBUG)
    loader = jinja2.FileSystemLoader(join(dirname(__file__), 'package.j2'))
    environment = jinja2.Environment(loader=loader)
    if 'desc' not in context or context['desc'] is None:
        context['desc'] = r'\[FIXME: Add better description!\]'
    if 'abbr' in context:
        context['abbr'] = '({})'.format(context['abbr'])
    for template in environment.list_templates(extensions='j2'):
        file_path, filename = os.path.split(template)
        if not add_tests and 'tests' in file_path:
            continue
        template = environment.get_template(template)
        out_path = join(path, file_path, splitext(filename)[0])
        if not isdir(split(out_path)[0]):
            logger.debug('+Dir  : %s', split(out_path)[0])
            if not dry_run:
                os.makedirs(split(out_path)[0])
        if not overwrite and isfile(out_path):
            logger.debug('* WARNING: Output already exists, skipping. '
                         '[%s]', out_path)
            continue
        logger.debug('+File : %s', out_path)
        if not dry_run:
            with open(out_path, 'w') as _file:
                _file.write(template.render(context))
    logger.debug('')


def is_leaf(config):
    """Return true if this is a leaf package."""
    for key, value in config.items():
        if isinstance(value, dict):
            return False
    return True


def create_context(config):
    """Create the Jinja2 template context dictionary the given configuration.

    Parameters
    ----------
    config : dict
        Configuration dictionary node for the package

    Returns
    -------
    dict
        Dictionary of Jinja2 template parameters
    """
    context = dict()
    for key, value in config.items():
        if not isinstance(value, dict):
            context[key] = value
    return context


def create_from_config(config, path=''):
    """Recursive method that crates packages from a configuration dictionary.

    Parameters
    ----------
    config : dict
        Package configuration dictionary
    path : str
        The current path
    """
    logger = logging.getLogger()
    for key, value in config.items():
        _path = join(path, key)
        if isinstance(value, dict):
            if len(config.keys()) == 1:
                logger.debug('Group   : %s', _path)
                create_from_config(value, _path)
            else:
                logger.debug('Package : %s', _path)
                context = create_context(value)
                create_package(_path, context, overwrite=False,
                               add_tests=is_leaf(value))
                create_from_config(value, _path)


def config_files():
    """Returns a list of config files."""
    config_path = join(dirname(__file__), 'config')
    return [join(config_path, file)
            for file in sorted(os.listdir(config_path))
            if file.endswith('.yaml')]


def create_packages():
    """Create packages from a set of configuration dictionaries"""
    logger = logging.getLogger()
    for config_file in config_files():
        logger.debug('%s', '-' * 80)
        logger.info('> Creating packages defined in: %s', config_file)
        logger.debug('%s', '-' * 80)
        with open(config_file) as stream:
            config = yaml.load(stream)
            create_from_config(config)


def main():
    """Main function."""
    parser = argparse.ArgumentParser('Create or destroy initial set of SIP '
                                     'packages.')
    parser.add_argument('-l', help="List Packages", action='store_true')
    parser.add_argument('-v', help="Verbose mode", action='store_true')
    args = parser.parse_args()

    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    if args.v:
        logger.setLevel(logging.DEBUG)

    if args.l:
        pass

    create_packages()


if __name__ == '__main__':
    main()
