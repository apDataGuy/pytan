
Create user
==========================================================================================

Create a user called API Test User

Example Python Code
----------------------------------------------------------------------------------------

.. code-block:: python
    :linenos:


    
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
    
    # setup the arguments for the delete method (to remove the package in case it exists)
    delete_kwargs = {}
    delete_kwargs["objtype"] = 'user'
    delete_kwargs["name"] = 'API Test User'
    
    
    # setup the arguments for the handler method
    kwargs = {}
    kwargs["username"] = u'API Test User'
    kwargs["rolename"] = u'Administrator'
    kwargs["properties"] = [[u'property1', u'value1']]
    
    # delete the object in case it already exists
    try:
        handler.delete(**delete_kwargs)
    except Exception as e:
        print e
    
    # call the handler with the create_user method, passing in kwargs for arguments
    response = handler.create_user(**kwargs)
    
    
    print ""
    print "Type of response: ", type(response)
    
    print ""
    print "print of response:"
    print response
    
    print ""
    print "print the object returned in JSON format:"
    print response.to_json(response)
    
    # delete the object, we are done with it now
    try:
        handler.delete(**delete_kwargs)
    except Exception as e:
        print e
    
    


Output from Python Code
----------------------------------------------------------------------------------------

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
    No results found searching for user with {'name': 'API Test User'}!!
    2015-03-26 11:49:18,767 INFO     handler: New user 'API Test User' created with ID 1015, roles: ['Administrator']
    
    Type of response:  <class 'taniumpy.object_types.user.User'>
    
    print of response:
    User, name: 'API Test User'
    
    print the object returned in JSON format:
    {
      "_type": "user", 
      "deleted_flag": 0, 
      "group_id": 0, 
      "id": 1015, 
      "last_login": "2001-01-01T00:00:00", 
      "metadata": {
        "_type": "metadata", 
        "item": [
          {
            "_type": "item", 
            "admin_flag": 0, 
            "name": "TConsole.User.Property.property1", 
            "value": "value1"
          }
        ]
      }, 
      "name": "API Test User", 
      "permissions": {
        "_type": "permissions", 
        "permission": "admin"
      }, 
      "roles": {
        "_type": "roles", 
        "role": [
          {
            "_type": "role", 
            "description": "Administrators can perform all functions in the system, including creating other users, viewing the System Status, changing Global Settings, and creating Computer Groups.", 
            "id": 1, 
            "name": "Administrator", 
            "permissions": {
              "_type": "permissions", 
              "permission": "admin"
            }
          }
        ]
      }
    }
    2015-03-26 11:49:18,797 INFO     handler: Deleted "User, name: 'API Test User'"
