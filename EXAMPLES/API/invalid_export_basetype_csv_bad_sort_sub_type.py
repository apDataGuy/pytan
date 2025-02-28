
"""
Export a BaseType from getting objects using a bad header_sort
"""

import os
import sys
sys.dont_write_bytecode = True

# Determine our script name, script dir
my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)

# determine the pytan lib dir and add it to the path
parent_dir = os.path.dirname(my_dir)
pytan_root_dir = os.path.dirname(parent_dir)
lib_dir = os.path.join(pytan_root_dir, 'lib')
path_adds = [lib_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)


# connection info for Tanium Server
USERNAME = "Tanium User"
PASSWORD = "T@n!um"
HOST = "172.16.31.128"
PORT = "444"

# Logging conrols
LOGLEVEL = 2
DEBUGFORMAT = False

import tempfile

import pytan
handler = pytan.Handler(
    username=USERNAME,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    loglevel=LOGLEVEL,
    debugformat=DEBUGFORMAT,
)

print handler

# setup the export_obj kwargs for later
export_kwargs = {}
export_kwargs["export_format"] = u'csv'
export_kwargs["header_sort"] = [[]]

# get the objects that will provide the basetype that we want to use
get_kwargs = {
    'name': [
        "Computer Name", "IP Route Details", "IP Address",
        'Folder Name Search with RegEx Match',
    ],
    'objtype': 'sensor',
}
response = handler.get(**get_kwargs)
export_kwargs['obj'] = response

# export the object to a string
# this should throw an exception: pytan.utils.HandlerError
import traceback

try:
    handler.export_obj(**export_kwargs)
except Exception as e:
    traceback.print_exc(file=sys.stdout)



'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
Traceback (most recent call last):
  File "<string>", line 66, in <module>
  File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 1435, in export_obj
    utils.check_dictkey(**check_args)
  File "/Users/jolsen/gh/pytan/lib/pytan/utils.py", line 2531, in check_dictkey
    raise HandlerError(err(key, valid_list_types, list_types))
HandlerError: 'header_sort' must be a list of [<type 'str'>, <type 'unicode'>], you supplied [<type 'list'>]!

'''
