# coding: utf-8
"""Module to create a SIP package.

This module uses jinja2 templates in the package.j2 directory
"""

import argparse
import os
from os.path import join
import jinja2


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Create new SIP package')
    parser.add_argument('PATH', help="Package Path")
    parser.add_argument('TITLE', help="Package title")
    parser.add_argument('-f',
                        help="Don't prompt for confirmation and over write "
                             "any existing package (USE WITH CARE!)",
                        action='store_true')
    args = parser.parse_args()

    _path = args.PATH
    _title = args.TITLE
    _force = args.f

    print('Path  = {}'.format(_path))
    print('Title = {}'.format(_title))

    if not _force and os.path.exists(_path):
        print('ERROR: Package already exists, exiting!')
        return

    loader = jinja2.FileSystemLoader(join(os.path.dirname(__file__), 'package.j2'))
    environment = jinja2.Environment(loader=loader)
    context = dict(title=_title, description=r'\[Add Description!\]')
    print('Templates:')
    for template in environment.list_templates(extensions='j2'):
        filepath, filename = os.path.split(template)
        template = environment.get_template(template)
        outpath = join(_path, filepath, os.path.splitext(filename)[0])
        if not os.path.isdir(os.path.split(outpath)[0]):
            print(' - Creating directory: {}'.format(os.path.split(outpath)[0]))
            os.makedirs(os.path.split(outpath)[0])
        print('   - IN : {}'.format(template.filename))
        print('   - OUT: {}'.format(outpath))
        with open(outpath, 'w') as _file:
            _file.write(template.render(context))

if __name__ == '__main__':
    main()
