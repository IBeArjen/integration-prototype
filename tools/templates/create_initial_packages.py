# -*- coding: utf-8 -*-
"""Script to create initial set of SIP packages.

Usage:

    python3 tools/templates/create_initial_packages.py [-c | -d]

"""
import argparse
import shutil
import os
from os.path import join
import json

import yaml

from create_sip_package import create_package


def is_package_valid(package):
    """Returns true if a package is valid.

    This is based on a list of required fields that need to exist and not be
    empty.

    Parameters
    ----------
    package : dict
        Package dictionary.
    """
    fields = ['title', 'path', 'desc', 'abbr']
    for field in fields:
        if not field in package:
            print('  * Found package with missing field: {}'.format(field))
            return False
        if package[field] is None:
            print('  * Found package with empty field: {}'.format(field))
            return False
    return True


def packages():
    """Returns a list of dictionaries describing the SIP packages.

    This is obtained from loading YAML files.
    """
    _path = os.path.dirname(__file__)
    config_path = join(_path, 'config')
    config_files = [join(config_path, file)
                    for file in sorted(os.listdir(config_path))
                    if file.endswith('.yaml')]
    package_list = list()
    for config_file in config_files:
        print('> Loading config:', config_file)
        package_count = 0
        with open(config_file, 'r') as stream:
            data = yaml.load(stream)
            root = data['package_root']
            if 'packages' not in data or data['packages'] is None:
                print('  - WARNING: No packages found, skipping.')
                continue
            for package in data['packages']:
                if is_package_valid(package):
                    package['path'] = join(*root, package['path'])
                    package_list.append(package)
                    package_count += 1
        print('  - {:d} Packages loaded'.format(package_count))
    return package_list


def create_packages():
    """Create all specfied SIP Packages."""
    for package in packages():
        package['path'] = os.path.join('sip', package['path'])
        print('--> Creating package: {}'.format(package['path']))
        create_package(package, overwrite=False)


def delete_packages():
    """Delete all specfied SIP Packages.

    ***WARNING*** USE WITH CARE!!
    """
    for package in packages():
        _path = os.path.join('sip', package['path'])
        if os.path.isdir(_path):
            print('--> Removing: {}'.format(_path))
            shutil.rmtree(_path)


def main():
    """Main function."""
    parser = argparse.ArgumentParser('Create or destroy initial set of SIP '
                                     'packages.')
    parser.add_argument('-c', help="Create Packages", action='store_true')
    parser.add_argument('-d', help="Delete Packages", action='store_true')
    parser.add_argument('-l', help="List Packages", action='store_true')
    args = parser.parse_args()
    if args.c and args.d:
        print('ERROR: Please select just one option, either -c, -d or -l!')
        return

    if args.c:
        create_packages()
    elif args.d:
        delete_packages()
    elif args.l:
        for index, package in enumerate(packages()):
            print('Package {:02d}'.format(index))
            print(json.dumps(package, indent=2))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
