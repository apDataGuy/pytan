
Invalid ask manual human question filter help
==========================================================================================

Have ask_manual_human() return the help for filters

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
    kwargs["filters_help"] = True
    kwargs["qtype"] = u'manual_human'
    
    
    # call the handler with the ask method, passing in kwargs for arguments
    # this should throw an exception: pytan.utils.PytanHelp
    import traceback
    try:
        handler.ask(**kwargs)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
    
    


Output from Python Code
----------------------------------------------------------------------------------------

.. code-block:: none
    :linenos:


    Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
    Traceback (most recent call last):
      File "<string>", line 55, in <module>
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 128, in ask
        result = getattr(self, q_obj_map['handler'])(**kwargs)
      File "/Users/jolsen/gh/pytan/lib/pytan/handler.py", line 379, in ask_manual_human
        raise PytanHelp(utils.help_filters())
    PytanHelp: 
    Filters Help
    ============
    
    Filters are used generously throughout pytan. When used as part of a
    sensor string, they control what data is shown for the columns that
    the sensor returns. When filters are used for whole question filters,
    they control what rows will be returned. They are used by Groups to
    define group membership, deploy actions to determine which machines
    should have the action deployed to it, and more.
    
    A filter string is a human string that describes, a sensor followed
    by ', that FILTER:VALUE', where FILTER is a valid filter string,
    and VALUE is the string that you want FILTER to match on.
    
    Valid Filters
    -------------
    
        '<'                      
            Help: Filter for less than VALUE
            Example: "Sensor1, that <:VALUE"
    
        'less'                   
            Help: Filter for less than VALUE
            Example: "Sensor1, that less:VALUE"
    
        'lt'                     
            Help: Filter for less than VALUE
            Example: "Sensor1, that lt:VALUE"
    
        'less than'              
            Help: Filter for less than VALUE
            Example: "Sensor1, that less than:VALUE"
    
        '!<'                     
            Help: Filter for not less than VALUE
            Example: "Sensor1, that !<:VALUE"
    
        'notless'                
            Help: Filter for not less than VALUE
            Example: "Sensor1, that notless:VALUE"
    
        'not less'               
            Help: Filter for not less than VALUE
            Example: "Sensor1, that not less:VALUE"
    
        'not less than'          
            Help: Filter for not less than VALUE
            Example: "Sensor1, that not less than:VALUE"
    
        '<='                     
            Help: Filter for less than or equal to VALUE
            Example: "Sensor1, that <=:VALUE"
    
        'less equal'             
            Help: Filter for less than or equal to VALUE
            Example: "Sensor1, that less equal:VALUE"
    
        'lessequal'              
            Help: Filter for less than or equal to VALUE
            Example: "Sensor1, that lessequal:VALUE"
    
        'le'                     
            Help: Filter for less than or equal to VALUE
            Example: "Sensor1, that le:VALUE"
    
        '!<='                    
            Help: Filter for not less than or equal to VALUE
            Example: "Sensor1, that !<=:VALUE"
    
        'not less equal'         
            Help: Filter for not less than or equal to VALUE
            Example: "Sensor1, that not less equal:VALUE"
    
        'not lessequal'          
            Help: Filter for not less than or equal to VALUE
            Example: "Sensor1, that not lessequal:VALUE"
    
        '>'                      
            Help: Filter for greater than VALUE
            Example: "Sensor1, that >:VALUE"
    
        'greater'                
            Help: Filter for greater than VALUE
            Example: "Sensor1, that greater:VALUE"
    
        'gt'                     
            Help: Filter for greater than VALUE
            Example: "Sensor1, that gt:VALUE"
    
        'greater than'           
            Help: Filter for greater than VALUE
            Example: "Sensor1, that greater than:VALUE"
    
        '!>'                     
            Help: Filter for not greater than VALUE
            Example: "Sensor1, that !>:VALUE"
    
        'not greater'            
            Help: Filter for not greater than VALUE
            Example: "Sensor1, that not greater:VALUE"
    
        'notgreater'             
            Help: Filter for not greater than VALUE
            Example: "Sensor1, that notgreater:VALUE"
    
        'not greater than'       
            Help: Filter for not greater than VALUE
            Example: "Sensor1, that not greater than:VALUE"
    
        '=>'                     
            Help: Filter for greater than or equal to VALUE
            Example: "Sensor1, that =>:VALUE"
    
        'greater equal'          
            Help: Filter for greater than or equal to VALUE
            Example: "Sensor1, that greater equal:VALUE"
    
        'greaterequal'           
            Help: Filter for greater than or equal to VALUE
            Example: "Sensor1, that greaterequal:VALUE"
    
        'ge'                     
            Help: Filter for greater than or equal to VALUE
            Example: "Sensor1, that ge:VALUE"
    
        '!=>'                    
            Help: Filter for not greater than VALUE
            Example: "Sensor1, that !=>:VALUE"
    
        'not greater equal'      
            Help: Filter for not greater than VALUE
            Example: "Sensor1, that not greater equal:VALUE"
    
        'notgreaterequal'        
            Help: Filter for not greater than VALUE
            Example: "Sensor1, that notgreaterequal:VALUE"
    
        '='                      
            Help: Filter for equals to VALUE
            Example: "Sensor1, that =:VALUE"
    
        'equal'                  
            Help: Filter for equals to VALUE
            Example: "Sensor1, that equal:VALUE"
    
        'equals'                 
            Help: Filter for equals to VALUE
            Example: "Sensor1, that equals:VALUE"
    
        'eq'                     
            Help: Filter for equals to VALUE
            Example: "Sensor1, that eq:VALUE"
    
        '!='                     
            Help: Filter for not equals to VALUE
            Example: "Sensor1, that !=:VALUE"
    
        'not equal'              
            Help: Filter for not equals to VALUE
            Example: "Sensor1, that not equal:VALUE"
    
        'notequal'               
            Help: Filter for not equals to VALUE
            Example: "Sensor1, that notequal:VALUE"
    
        'not equals'             
            Help: Filter for not equals to VALUE
            Example: "Sensor1, that not equals:VALUE"
    
        'notequals'              
            Help: Filter for not equals to VALUE
            Example: "Sensor1, that notequals:VALUE"
    
        'ne'                     
            Help: Filter for not equals to VALUE
            Example: "Sensor1, that ne:VALUE"
    
        'contains'               
            Help: Filter for contains VALUE (adds .* before and after VALUE)
            Example: "Sensor1, that contains:VALUE"
    
        'does not contain'       
            Help: Filter for does not contain VALUE (adds .* before and after VALUE)
            Example: "Sensor1, that does not contain:VALUE"
    
        'doesnotcontain'         
            Help: Filter for does not contain VALUE (adds .* before and after VALUE)
            Example: "Sensor1, that doesnotcontain:VALUE"
    
        'not contains'           
            Help: Filter for does not contain VALUE (adds .* before and after VALUE)
            Example: "Sensor1, that not contains:VALUE"
    
        'notcontains'            
            Help: Filter for does not contain VALUE (adds .* before and after VALUE)
            Example: "Sensor1, that notcontains:VALUE"
    
        'starts with'            
            Help: Filter for starts with VALUE (adds .* after VALUE)
            Example: "Sensor1, that starts with:VALUE"
    
        'startswith'             
            Help: Filter for starts with VALUE (adds .* after VALUE)
            Example: "Sensor1, that startswith:VALUE"
    
        'does not start with'    
            Help: Filter for does not start with VALUE (adds .* after VALUE)
            Example: "Sensor1, that does not start with:VALUE"
    
        'doesnotstartwith'       
            Help: Filter for does not start with VALUE (adds .* after VALUE)
            Example: "Sensor1, that doesnotstartwith:VALUE"
    
        'not starts with'        
            Help: Filter for does not start with VALUE (adds .* after VALUE)
            Example: "Sensor1, that not starts with:VALUE"
    
        'notstartswith'          
            Help: Filter for does not start with VALUE (adds .* after VALUE)
            Example: "Sensor1, that notstartswith:VALUE"
    
        'ends with'              
            Help: Filter for ends with VALUE (adds .* before VALUE)
            Example: "Sensor1, that ends with:VALUE"
    
        'endswith'               
            Help: Filter for ends with VALUE (adds .* before VALUE)
            Example: "Sensor1, that endswith:VALUE"
    
        'does not end with'      
            Help: Filter for does bit end with VALUE (adds .* before VALUE)
            Example: "Sensor1, that does not end with:VALUE"
    
        'doesnotendwith'         
            Help: Filter for does bit end with VALUE (adds .* before VALUE)
            Example: "Sensor1, that doesnotendwith:VALUE"
    
        'not ends with'          
            Help: Filter for does bit end with VALUE (adds .* before VALUE)
            Example: "Sensor1, that not ends with:VALUE"
    
        'notstartswith'          
            Help: Filter for does bit end with VALUE (adds .* before VALUE)
            Example: "Sensor1, that notstartswith:VALUE"
    
        'is not'                 
            Help: Filter for non regular expression match for VALUE
            Example: "Sensor1, that is not:VALUE"
    
        'not regex'              
            Help: Filter for non regular expression match for VALUE
            Example: "Sensor1, that not regex:VALUE"
    
        'notregex'               
            Help: Filter for non regular expression match for VALUE
            Example: "Sensor1, that notregex:VALUE"
    
        'not regex match'        
            Help: Filter for non regular expression match for VALUE
            Example: "Sensor1, that not regex match:VALUE"
    
        'notregexmatch'          
            Help: Filter for non regular expression match for VALUE
            Example: "Sensor1, that notregexmatch:VALUE"
    
        'nre'                    
            Help: Filter for non regular expression match for VALUE
            Example: "Sensor1, that nre:VALUE"
    
        'is'                     
            Help: Filter for regular expression match for VALUE
            Example: "Sensor1, that is:VALUE"
    
        'regex'                  
            Help: Filter for regular expression match for VALUE
            Example: "Sensor1, that regex:VALUE"
    
        'regex match'            
            Help: Filter for regular expression match for VALUE
            Example: "Sensor1, that regex match:VALUE"
    
        'regexmatch'             
            Help: Filter for regular expression match for VALUE
            Example: "Sensor1, that regexmatch:VALUE"
    
        're'                     
            Help: Filter for regular expression match for VALUE
            Example: "Sensor1, that re:VALUE"
    
    
