Ask Saved Question Readme
===========================

---------------------------
<a name='toc'>Table of contents:</a>

  * [Ask Saved Question Help](#user-content-ask-saved-question-help)
  * [Ask a saved question](#user-content-ask-a-saved-question)

---------------------------

# Ask Saved Question Help

  * Ask a saved question and save the results as a report format

```bash
ask_saved_question.py -h
```

```
usage: ask_saved_question.py [-h] [-u USERNAME] [-p PASSWORD] [--host HOST]
                             [--port PORT] [-l LOGLEVEL]
                             [--id ID | --name NAME] [--file REPORT_FILE]
                             [--dir REPORT_DIR]
                             {csv,json} ...

Ask a saved question and save the results as a report format

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

Saved Question Selectors:
  --id ID               id of saved_question to ask (default: None)
  --name NAME           name of saved_question to ask (default: None)

Report File Options:
  --file REPORT_FILE    File to save report to (will be automatically
                        generated if not supplied) (default: None)
  --dir REPORT_DIR      Directory to save report to (current directory will be
                        used if not supplied) (default: None)

Export Formats:
  {csv,json}            Export Format choices
    csv                 Produce a CSV report, supply "csv -h" to see CSV
                        options
    json                Produce a JSON report, supply "json -h" to see JSON
                        options

usage: ask_saved_question.py csv [-h]
                                 [--sort HEADER_SORT | --no-sort | --auto_sort]
                                 [--add-sensor | --no-add-sensor]
                                 [--add-type | --no-add-type]
                                 [--expand-columns | --no-columns]

CSV Export Options

optional arguments:
  -h, --help          show this help message and exit
  --sort HEADER_SORT  Sort headers by given names (default: [])
  --no-sort           Do not sort the headers at all
  --auto_sort         Sort the headers with a basic alphanumeric sort
                      (default)
  --add-sensor        Add the sensor names to each header
  --no-add-sensor     Do not add the sensor names to each header (default)
  --add-type          Add the result type to each header
  --no-add-type       Do not add the result type to each header (default)
  --expand-columns    Expand multi-line cells into their own rows that have
                      sensor correlated columns in the new rows
  --no-columns        Do not add expand multi-line cells into their own rows
                      (default)

usage: ask_saved_question.py json [-h]

JSON Export Options

optional arguments:
  -h, --help  show this help message and exit
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0



[TOC](#user-content-toc)


# Ask a saved question

```bash
ask_saved_question.py -u 'Tanium User' -p 'T@n!um' --host '172.16.31.128' --loglevel 1 --name "Installed Applications" --file "/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv" csv
```

```
Handler for Session to 172.16.31.128:444, Authenticated: True, Version: 6.2.314.3279
++ Asking saved question: Installed Applications
2015-03-26 09:26:17,641 INFO     question_progress: Results 100% (Get Installed Applications from all machines)
++ Saved Question 'Get Installed Applications from all machines' ID: 92
Report file '/var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv' written with 21914 bytes
```

  * Validation Test: exitcode
    * Valid: **True**
    * Messages: Exit Code is 0

  * Validation Test: file_exist_contents
    * Valid: **True**
    * Messages: File /var/folders/dk/vjr1r_c53yx6k6gzp2bbt_c40000gn/T/out.csv exists, content:

```
Name,Silent Uninstall String,Uninstallable,Version
Google Search,nothing,Not Uninstallable,37.0.2062.120
Microsoft Chart Converter,nothing,Not Uninstallable,14.4.7
Wish,nothing,Not Uninstallable,8.5.9
BluetoothUIServer,nothing,Not Uninstallable,4.3.2
Time Machine,nothing,Not Uninstallable,1.3
AppleGraphicsWarning,nothing,Not Uninstallable,2.3.0
Python 2.7 py2exe-0.6.9,"""C:\Python27\Removepy2exe.exe"" -u ""C:\Python27\py2exe-wininst.log""",Not Uninstallable,-0.6.9
soagent,nothing,Not Uninstallable,7.0
AinuIM,nothing,Not Uninstallable,1.0
...trimmed for brevity...
```



[TOC](#user-content-toc)


###### generated by: `build_bin_doc v1.4.5`, date: Thu Mar 26 09:26:17 2015 EDT, Contact info: **Jim Olsen <jim.olsen@tanium.com>**