Tanium Unmanaged Asset Tracker Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Tanium Unmanaged Asset Tracker Help](#user-content-tanium-unmanaged-asset-tracker-help)

---------------------------

# Tanium Unmanaged Asset Tracker Help

  * TUAT: Compares Unmanaged Asset data against Tanium Clients in System Status

```bash
Tanium_Unmanaged_Asset_Tracker.py -h
```

```
usage: Tanium_Unmanaged_Asset_Tracker.py [-h] [-u USERNAME] [-p PASSWORD]
                                         [--host HOST] [--port PORT]
                                         [-l LOGLEVEL] [--debugformat]
                                         [--output_dir REPORT_DIR]
                                         [--pct PCT_COMPLETE_THRESHOLD]
                                         [--timeout TIMEOUT]
                                         [--max_data_age MAX_DATA_AGE]
                                         [--saved]
                                         [--last_registration_hours LAST_REGISTRATION_HOURS]

TUAT: Compares Unmanaged Asset data against Tanium Clients in System Status

optional arguments:
  -h, --help            show this help message and exit

Tanium Authentication:
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
  --debugformat         Log with debug level to console and files (default:
                        False)

TUAT Options:
  --output_dir REPORT_DIR
                        Directory to save output to (default: /Users/jolsen/gh
                        /pytan/BUILD/TUAT_OUTPUT/2015_03_26-09_28_45-EDT)
  --pct PCT_COMPLETE_THRESHOLD
                        Percent to consider questions complete (default: 99.0)
  --timeout TIMEOUT     How many seconds to wait before a question times out
                        (default: 300)
  --max_data_age MAX_DATA_AGE
                        Maximum age of client data in seconds, refresh if
                        cached data is older than this (default: 60)
  --saved               Used the saved question data for Unmanaged Assets
                        instead of asking a brand new question (default:
                        False)
  --last_registration_hours LAST_REGISTRATION_HOURS
                        When fetching Managed Assets, fetch only clients that
                        have reported in the last N hours (default: 12)
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Thu Mar 26 09:28:45 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**