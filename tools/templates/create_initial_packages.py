# -*- coding: utf-8 -*-
"""Script to create initial set of SIP packages.

Usage:

    python3 tools/templates/create_initial_packages.py [-c | -d]

"""
import argparse
import shutil
import os

from create_sip_package import create_package


def packages():
    """Returns a list of dictionaries describing the SIP packages."""
    return [
        # Execution control
        {
            'path': 'execution_control/master_rpc',
            'acronym': 'mc_rpc',
            'title': 'Master Controller',
            'desc': 'SDP Element Master with an RPC endpoint'
        },
        {
            'path': 'execution_control/master_tango',
            'acronym': 'mc_tango',
            'title': 'Tango SDP Element Master',
            'desc': 'The SDP baseline Tango SDP Element Master'
        },
        {
            'path': 'execution_control/processing_control_rpc',
            'acronym': 'pctl_rpc',
            'title': 'RPC Processing Controller',
            'desc': 'Processing controller with an RPC endpoint'
        },
        {
            'path': 'execution_control/processing_control_tango',
            'acronym': 'pctl_tango',
            'title': 'Tango Processing controller',
            'desc': 'Tango Processing controller'
        },
        {
            'path': 'execution_control/simple_monitoring_service',
            'acronym': 'mon',
            'title': 'Monitoring Service'
        },
        {
            'path': 'execution_control/simple_config_service',
            'acronym': 'scs_redis',
            'title': 'Simple Redis Configuration Service',
            'desc': 'A simple Redis configuration service API'
        },
        # SDP Services
        {
            'path': 'execution_control/quality_assessment_tango',
            'acronym': 'qa_tango',
            'title': 'Quality Assessment Service',
        },

    ]


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
    parser.add_argument('-c', help="Create Pacakages", action='store_true')
    parser.add_argument('-d', help="Delete Pacakages", action='store_true')
    args = parser.parse_args()
    if args.c and args.d:
        print('ERROR: Please select just one option, either -c or -d!')
        return

    if args.c:
        create_packages()
    elif args.d:
        delete_packages()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
