# -*- coding: utf-8 -*-
"""Script to create initial set of SIP packages.

Usage:

    python3 tools/templates/create_initial_packages.py [-c | -d]

"""
import argparse
import shutil
import os
from os.path import join, dirname, split, splitext, isfile
import json
import logging

import jinja2
import yaml


def create_package(path, context, overwrite=False, add_tests=True):
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
        if not os.path.isdir(split(out_path)[0]):
            logger.debug('  - Creating directory : %s', split(out_path)[0])
            os.makedirs(split(out_path)[0])
        if not overwrite and isfile(out_path):
            logger.warning('    **WARNING** Output already exists, skipping. '
                           '[%s]', out_path)
            continue
        with open(out_path, 'w') as _file:
            logger.debug('    - Template : %s', template.filename)
            logger.debug('    - Output   : %s', out_path)
            _file.write(template.render(context))


def config_files():
    """Returns a list of config files."""
    config_path = join(dirname(__file__), 'config')
    return [join(config_path, file)
            for file in sorted(os.listdir(config_path))
            if file.endswith('.yaml')]


def is_leaf(config):
    """Return true if this is a leaf package."""
    for key, value in config.items():
        if isinstance(value, dict):
            return False
    return True


def create_context(config):
    """Create template context from configuration."""
    context = dict()
    for key, value in config.items():
        if not isinstance(value, dict):
            context[key] = value
    return context


def create_from_config(config, path=''):
    """Create Packages from configuration."""
    logger = logging.getLogger()
    for key, value in config.items():
        _path = join(path, key)
        if isinstance(value, dict):
            if len(config.keys()) == 1:
                logger.debug('GROUP: %s', _path)
                create_from_config(value, _path)
            else:
                logger.debug('PACKAGE: %s', _path)
                context = create_context(value)
                # print(is_leaf(value))
                # print(json.dumps(context, indent=2))
                create_package(_path, context, overwrite=False,
                               add_tests=is_leaf(value))
                create_from_config(value, _path)


def create_packages():
    """Create packages."""
    for config_file in config_files():
        if '01' not in config_file:
            continue
        print('> Loading config:', config_file)
        with open(config_file) as stream:
            config = yaml.load(stream)
            create_from_config(config)


# def is_package_valid(package):
#     """Returns true if a package is valid.
#
#     This is based on a list of required fields that need to exist and not be
#     empty.
#
#     Parameters
#     ----------
#     package : dict
#         Package dictionary.
#     """
#     fields = ['title', 'path', 'desc', 'abbr']
#     for field in fields:
#         if not field in package:
#             print('  * Found package with missing field: {}'.format(field))
#             return False
#         if package[field] is None:
#             print('  * Found package with empty field: {}'.format(field))
#             return False
#     return True
#
#
# def packages():
#     """Returns a list of dictionaries describing the SIP packages.
#
#     This is obtained from loading YAML files.
#     """
#     _path = os.path.dirname(__file__)
#     config_path = join(_path, 'config')
#     config_files = [join(config_path, file)
#                     for file in sorted(os.listdir(config_path))
#                     if file.endswith('.yaml')]
#     package_list = list()
#     for config_file in config_files:
#         print('> Loading config:', config_file)
#         package_count = 0
#         with open(config_file, 'r') as stream:
#             data = yaml.load(stream)
#             root = data['package_root']
#             if 'packages' not in data or data['packages'] is None:
#                 print('  - WARNING: No packages found, skipping.')
#                 continue
#             for package in data['packages']:
#                 if is_package_valid(package):
#                     package['path'] = join(*root, package['path'])
#                     package_list.append(package)
#                     package_count += 1
#         print('  - {:d} Packages loaded'.format(package_count))
#     return package_list
#
#
# def create_packages():
#     """Create all specfied SIP Packages."""
#     for package in packages():
#         package['path'] = os.path.join('sip', package['path'])
#         print('--> Creating package: {}'.format(package['path']))
#         create_package(package, overwrite=False)
#
#
# def delete_packages():
#     """Delete all specfied SIP Packages.
#
#     ***WARNING*** USE WITH CARE!!
#     """
#     for package in packages():
#         _path = os.path.join('sip', package['path'])
#         if os.path.isdir(_path):
#             print('--> Removing: {}'.format(_path))
#             shutil.rmtree(_path)


def main():
    """Main function."""
    parser = argparse.ArgumentParser('Create or destroy initial set of SIP '
                                     'packages.')
    parser.add_argument('-c', help="Create Packages", action='store_true')
    parser.add_argument('-d', help="Delete Packages", action='store_true')
    parser.add_argument('-l', help="List Packages", action='store_true')
    parser.add_argument('-v', help="Verbose mode", action='store_true')
    args = parser.parse_args()
    if args.c and args.d:
        print('ERROR: Please select just one option, either -c, -d or -l!')
        return

    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    if args.v:
        logger.setLevel(logging.DEBUG)

    if args.l:
        pass

    if args.c:
        create_packages()
    elif args.d:
        # delete_packages()
        pass
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
