
Get leader clients
==========================================================================================

Get all clients that are Leader status

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
    
    # setup the arguments for the handler method
    kwargs = {}
    kwargs["objtype"] = u'client'
    kwargs["status"] = u'Leader'
    
    # call the handler with the get method, passing in kwargs for arguments
    response = handler.get(**kwargs)
    
    print ""
    print "Type of response: ", type(response)
    
    print ""
    print "print of response:"
    print response
    
    print ""
    print "length of response (number of objects returned): "
    print len(response)
    
    print ""
    print "print the first object returned in JSON format:"
    out = response.to_json(response[0])
    if len(out.splitlines()) > 15:
        out = out.splitlines()[0:15]
        out.append('..trimmed for brevity..')
        out = '\n'.join(out)
    
    print out
    
    


Output from Python Code
----------------------------------------------------------------------------------------

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
    
    Type of response:  <class 'taniumpy.object_types.system_status_list.SystemStatusList'>
    
    print of response:
    SystemStatusList, len: 4
    
    length of response (number of objects returned): 
    4
    
    print the first object returned in JSON format:
    {
      "_type": "client_status", 
      "cache_row_id": 1, 
      "computer_id": "103801052", 
      "full_version": "6.0.314.1195", 
      "host_name": "WIN-A12SC6N6T7Q", 
      "ipaddress_client": "172.16.31.157", 
      "ipaddress_server": "172.16.31.157", 
      "last_registration": "2015-03-11T09:30:02", 
      "port_number": 17472, 
      "protocol_version": 314, 
      "receive_state": "Previous Only", 
      "send_state": "Backward Only", 
      "status": "Leader"
    }
