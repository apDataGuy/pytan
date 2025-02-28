Create Sensor From Json Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Create Sensor From Json Help](#user-content-create-sensor-from-json-help)
  * [Export sensor id 1 as JSON](#user-content-export-sensor-id-1-as-json)
  * [Change name or url_regex in the JSON](#user-content-change-name-or-url_regex-in-the-json)
  * [Create a new sensor from the modified JSON file](#user-content-create-a-new-sensor-from-the-modified-json-file)

---------------------------

# Create Sensor From Json Help

  * Create a sensor object from a json file

```bash
create_sensor_from_json.py -h
```

```
usage: create_sensor_from_json.py [-h] [-u USERNAME] [-p PASSWORD]
                                  [--host HOST] [--port PORT] [-l LOGLEVEL] -j
                                  JSON_FILE

Create a sensor object from a json file

optional arguments:
  -h, --help            show this help message and exit

Handler Authentication:
  -u USERNAME, --username USERNAME
                        Name of user (default: None)
  -p PASSWORD, --password PASSWORD
                        Password of user (default: None)
  --host HOST           Hostname/ip of SOAP Server (default: None)
  --port PORT           Port to use when connecting to SOAP Server (default:
                        444)

Handler Options:
  -l LOGLEVEL, --loglevel LOGLEVEL
                        Logging level to use, increase for more verbosity
                        (default: 0)

Create Sensor from JSON Options:
  -j JSON_FILE, --json JSON_FILE
                        JSON file to use for creating the object (default: )
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


# Export sensor id 1 as JSON

  * Get the first sensor object
  * Save the results to a JSON file

```bash
get_sensor.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --id 1 --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json" json
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
Found items:  SensorList, len: 1
Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json' written with 781 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json exists, content:

```
{
  "_type": "sensors", 
  "sensor": [
    {
      "_type": "sensor", 
      "category": "Reserved", 
      "description": "The recorded state of each action a client has taken recently in the form of id:status.\nExample: 1:Completed", 
      "exclude_from_parse_flag": 1, 
      "hash": 1792443391, 
      "hidden_flag": 0, 
...trimmed for brevity...
```



[TOC](#user-content-toc)


# Change name or url_regex in the JSON

  * Add CMDLINE TEST to name or url_regex in the JSON file

```bash
perl -p -i -e 's/^(      "(name|url_regex)": ".*)"/$1 CMDLINE TEST 2083"/gm' /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json && cat /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json
```

```
{
  "_type": "sensors", 
  "sensor": [
    {
      "_type": "sensor", 
      "category": "Reserved", 
      "description": "The recorded state of each action a client has taken recently in the form of id:status.\nExample: 1:Completed", 
      "exclude_from_parse_flag": 1, 
      "hash": 1792443391, 
      "hidden_flag": 0, 
      "id": 1, 
      "ignore_case_flag": 1, 
      "max_age_seconds": 3600, 
      "name": "Action Statuses CMDLINE TEST 2083", 
      "queries": {
        "_type": "queries", 
        "query": [
          {
            "_type": "query", 
            "platform": "Windows", 
            "script": "Reserved", 
            "script_type": "WMIQuery"
          }
        ]
      }, 
      "source_id": 0, 
      "string_count": 7100, 
      "value_type": "String"
    }
  ]
}
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json exists



[TOC](#user-content-toc)


# Create a new sensor from the modified JSON file

```bash
create_sensor_from_json.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 -j "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json"
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
Created item: Sensor, name: 'Action Statuses CMDLINE TEST 2083', ID: 1826
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Thu Mar 26 09:26:23 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**