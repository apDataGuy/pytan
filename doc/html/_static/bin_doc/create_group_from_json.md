Create Group From Json Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Create Group From Json Help](#user-content-create-group-from-json-help)
  * [Export group id 1 as JSON](#user-content-export-group-id-1-as-json)
  * [Change name or url_regex in the JSON](#user-content-change-name-or-url_regex-in-the-json)
  * [Create a new group from the modified JSON file](#user-content-create-a-new-group-from-the-modified-json-file)

---------------------------

# Create Group From Json Help

  * Create a group object from a json file

```bash
create_group_from_json.py -h
```

```
usage: create_group_from_json.py [-h] [-u USERNAME] [-p PASSWORD]
                                 [--host HOST] [--port PORT] [-l LOGLEVEL] -j
                                 JSON_FILE

Create a group object from a json file

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

Create Group from JSON Options:
  -j JSON_FILE, --json JSON_FILE
                        JSON file to use for creating the object (default: )
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


# Export group id 1 as JSON

  * Get the first group object
  * Save the results to a JSON file

```bash
get_group.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --id 1 --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json" json
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
Found items:  GroupList, len: 1
Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json' written with 1024 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json exists, content:

```
{
  "_type": "groups", 
  "group": [
    {
      "_type": "group", 
      "and_flag": 1, 
      "deleted_flag": 0, 
      "filters": {
        "_type": "filters", 
        "filter": [
...trimmed for brevity...
```



[TOC](#user-content-toc)


# Change name or url_regex in the JSON

  * Add CMDLINE TEST to name or url_regex in the JSON file

```bash
perl -p -i -e 's/^(      "(name|url_regex)": ".*)"/$1 CMDLINE TEST 1591"/gm' /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json && cat /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json
```

```
{
  "_type": "groups", 
  "group": [
    {
      "_type": "group", 
      "and_flag": 1, 
      "deleted_flag": 0, 
      "filters": {
        "_type": "filters", 
        "filter": [
          {
            "_type": "filter", 
            "all_times_flag": 0, 
            "all_values_flag": 0, 
            "delimiter_index": 0, 
            "ignore_case_flag": 1, 
            "max_age_seconds": 0, 
            "not_flag": 0, 
            "operator": "RegexMatch", 
            "sensor": {
              "_type": "sensor", 
              "hash": 1569955801
            }, 
            "substring_flag": 0, 
            "substring_length": 0, 
            "substring_start": 0, 
            "utf8_flag": 0, 
            "value": ".*open.*", 
            "value_type": "String"
          }
        ]
      }, 
      "id": 1, 
      "not_flag": 0, 
      "sub_groups": {
        "_type": "groups", 
        "group": []
      }, 
      "text": " Unencrypted Wireless Networks contains \"open\"", 
      "type": 0
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


# Create a new group from the modified JSON file

```bash
create_group_from_json.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 -j "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.json"
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
Created item: Group, id: 19133, ID: 19133
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Thu Mar 26 09:26:19 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**