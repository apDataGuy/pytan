#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Create a user object from command line arguments'''
__author__ = 'Jim Olsen (jim.olsen@tanium.com)'
__version__ = '1.0.4'

import os
import sys
import getpass
sys.dont_write_bytecode = True
my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
lib_dir = os.path.join(parent_dir, 'lib')
path_adds = [lib_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)

import pytan
from pytan import utils


examples = [
    {
        'name': 'Create a new user',
        'cmd': (
            'create_user.py $API_INFO --name "CMDLINE TEST user" '
            '--rolename "Administrator" '
            '--property "property name" "property value" | tee -a $TMP/create_user.out'
        ),
        'notes': [
            'Create a user named CMDLINE TEST user',
            'Assign the Administrator role to the new user',
            'Create a property named property name with the value property value on the new user',
        ],
        'precleanup': 'rm -f $TMP/create_user.out',
        'tests': 'exitcode',
    },
    {
        'name': 'Delete the recently created user',
        'cmd': (
            """delete_user.py $API_INFO """
            """--id `cat $TMP/create_user.out| grep created | sed 's/.*ID //' | cut -d, -f1` """
        ),
        'notes': [
            'Delete the user named CMDLINE TEST user',
        ],
        'tests': 'exitcode',
    },
]


def process_handler_args(parser, all_args):
    handler_grp_names = ['Handler Authentication', 'Handler Options']
    handler_opts = utils.get_grp_opts(parser, handler_grp_names)
    handler_args = {k: all_args.pop(k) for k in handler_opts}

    try:
        h = pytan.Handler(**handler_args)
        print str(h)
    except Exception as e:
        print e
        sys.exit(99)
    return h


if __name__ == "__main__":

    utils.version_check(__version__)
    parser = utils.setup_parser(__doc__, True)
    arggroup = parser.add_argument_group('Create User Options')

    arggroup.add_argument(
        '-n',
        '--name',
        required=True,
        action='store',
        dest='name',
        default=None,
        help='Name of user to create',
    )

    arggroup.add_argument(
        '-rn',
        '--rolename',
        required=False,
        action='append',
        dest='rolename',
        default=[],
        help='Name of role to assign to new user',
    )

    arggroup.add_argument(
        '-ri',
        '--roleid',
        required=False,
        action='append',
        type=int,
        dest='roleid',
        default=[],
        help='ID of role to assign to new user',
    )

    arggroup.add_argument(
        '-prop',
        '--property',
        required=False,
        action='append',
        dest='properties',
        nargs=2,
        default=[],
        help='Property name and value to assign to user',
    )

    args = parser.parse_args()
    all_args = args.__dict__
    if not args.username:
        username = raw_input('Tanium Username: ')
        all_args['username'] = username.strip()

    if not args.password:
        password = getpass.getpass('Tanium Password: ')
        all_args['password'] = password.strip()

    if not args.host:
        host = raw_input('Tanium Host: ')
        all_args['host'] = host.strip()

    handler = process_handler_args(parser, all_args)
    try:
        user_obj = handler.create_user(
            username=args.name,
            rolename=args.rolename,
            roleid=args.roleid,
            properties=args.properties,
        )
        m = "New user {!r} created with ID {!r}, roles: {!r}".format
        print(m(
            user_obj.name, user_obj.id, ', '.join([x.name for x in user_obj.roles])
        ))
    except Exception as e:
        print e
        sys.exit(99)
