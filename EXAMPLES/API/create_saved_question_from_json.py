
"""
Export a saved question object to a JSON file, adding ' API TEST' to the name of the saved question before exporting the JSON file and deleting any pre-existing saved question with the same (new) name, then create a new saved question object from the exported JSON file
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

# set the attribute name and value we want to add to the original object (if any)
attr_name = "name"
attr_add = " API TEST"

# delete object before creating it?
delete = True

# setup the arguments for getting an object to export as json file
get_kwargs = {}
get_kwargs["objtype"] = u'saved_question'
get_kwargs["id"] = 1


# get objects to use as an export to JSON file
orig_objs = handler.get(**get_kwargs)

# if attr_name and attr_add exists, modify the orig_objs to add attr_add to the attribute
# attr_name
if attr_name:
    for x in orig_objs:
        new_attr = getattr(x, attr_name)
        new_attr += attr_add
        setattr(x, attr_name, new_attr)
        if delete:
            # delete the object in case it already exists
            del_kwargs = {}
            del_kwargs[attr_name] = new_attr
            del_kwargs['objtype'] = u'saved_question'
            try:
                handler.delete(**del_kwargs)
            except Exception as e:
                print e

# export orig_objs to a json file
json_file, results = handler.export_to_report_file(
    obj=orig_objs,
    export_format='json',
    report_dir=tempfile.gettempdir(),
)

# create the object from the exported JSON file
create_kwargs = {'objtype': u'saved_question', 'json_file': json_file}
response = handler.create_from_json(**create_kwargs)


print ""
print "Type of response: ", type(response)

print ""
print "print of response:"
print response

print ""
print "print the object returned in JSON format:"
print response.to_json(response)


'''Output from running this:
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
2015-03-26 11:49:19,419 INFO     handler: Deleted 'SavedQuestion, id: 11657'
2015-03-26 11:49:19,421 INFO     handler: Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/SavedQuestionList_2015_03_26-11_49_19-EDT.json' written with 4601 bytes
2015-03-26 11:49:19,457 INFO     handler: New SavedQuestion, name: 'Run Unmanaged Asset Scan on All Machines API TEST' (ID: 11658) created successfully!

Type of response:  <class 'taniumpy.object_types.saved_question_list.SavedQuestionList'>

print of response:
SavedQuestionList, len: 1

print the object returned in JSON format:
{
  "_type": "saved_questions", 
  "saved_question": [
    {
      "_type": "saved_question", 
      "action_tracking_flag": 0, 
      "archive_enabled_flag": 0, 
      "archive_owner": {
        "_type": "user"
      }, 
      "expire_seconds": 600, 
      "hidden_flag": 0, 
      "id": 11658, 
      "issue_seconds": 120, 
      "issue_seconds_never_flag": 0, 
      "keep_seconds": 0, 
      "mod_time": "2000-01-01T00:00:00", 
      "most_recent_question_id": 32605, 
      "name": "Run Unmanaged Asset Scan on All Machines API TEST", 
      "packages": {
        "_type": "package_specs", 
        "package_spec": []
      }, 
      "public_flag": 1, 
      "query_text": "Get Is Windows from all machines", 
      "question": {
        "_type": "question", 
        "action_tracking_flag": 0, 
        "expiration": "2015-03-26T15:16:00", 
        "expire_seconds": 0, 
        "force_computer_id_flag": 0, 
        "hidden_flag": 0, 
        "id": 32605, 
        "management_rights_group": {
          "_type": "group", 
          "id": 0
        }, 
        "query_text": "Get Is Windows from all machines", 
        "saved_question": {
          "_type": "saved_question", 
          "id": 11658
        }, 
        "selects": {
          "_type": "selects", 
          "select": [
            {
              "_type": "select", 
              "filter": {
                "_type": "filter", 
                "all_times_flag": 0, 
                "all_values_flag": 0, 
                "delimiter_index": 0, 
                "end_time": "2001-01-01T00:00:00", 
                "ignore_case_flag": 1, 
                "max_age_seconds": 0, 
                "not_flag": 0, 
                "operator": "Less", 
                "start_time": "2001-01-01T00:00:00", 
                "substring_flag": 0, 
                "substring_length": 0, 
                "substring_start": 0, 
                "utf8_flag": 0, 
                "value_type": "String"
              }, 
              "sensor": {
                "_type": "sensor", 
                "category": "Operating System", 
                "creation_time": "2015-03-03T19:03:34", 
                "delimiter": ",", 
                "description": "Returns whether the machine runs Windows.  True if so, False if not.\nExample: True", 
                "exclude_from_parse_flag": 0, 
                "hash": 2721439124, 
                "hidden_flag": 0, 
                "id": 35, 
                "ignore_case_flag": 1, 
                "last_modified_by": "Jim Olsen", 
                "max_age_seconds": 86400, 
                "metadata": {
                  "_type": "metadata", 
                  "item": [
                    {
                      "_type": "item", 
                      "admin_flag": 0, 
                      "name": "defined", 
                      "value": "Tanium"
                    }
                  ]
                }, 
                "modification_time": "2015-03-03T19:03:34", 
                "name": "Is Windows", 
                "queries": {
                  "_type": "queries", 
                  "query": [
                    {
                      "_type": "query", 
                      "platform": "Windows", 
                      "script": "&#039;========================================\n&#039; Is Windows\n&#039;========================================\n\nWscript.echo &quot;True&quot;", 
                      "script_type": "VBScript"
                    }, 
                    {
                      "_type": "query", 
                      "platform": "Linux", 
                      "script": "#!/bin/bash\necho False\n", 
                      "script_type": "UnixShell"
                    }, 
                    {
                      "_type": "query", 
                      "platform": "Mac", 
                      "script": "#!/bin/bash\necho False\n", 
                      "script_type": "UnixShell"
                    }
                  ]
                }, 
                "source_id": 0, 
                "string_count": 3, 
                "value_type": "String"
              }
            }
          ]
        }, 
        "skip_lock_flag": 0, 
        "user": {
          "_type": "user", 
          "id": 1, 
          "name": "Jim Olsen"
        }
      }, 
      "row_count_flag": 0, 
      "sort_column": 0, 
      "user": {
        "_type": "user", 
        "id": 2, 
        "name": "Tanium User"
      }
    }
  ]
}

'''
