# cnm-usage

CLI app to pull usage/performance data from cnMaestro API. It calls /api/v1/devices/performance and pulls a maximum of 100 entries per call, within a time window starting at most one week ago.

**Note:** Full functionality from the command line is not supported. The code will need to be edited directly to change some settings, such as request limits and offsets. This program should be further developed before it is used.

## Installation
This package must be manually installed by running the included setup.py script. Run this command while inside the cnm-usage directory:
      \> python3 setup.py install
It is recommended to install inside of a python virtual environment, such as venv. 

## Usage
  #### Command:
    cnm_usage [ -i \<client id> ] [ -s \<client secret> ] [ -p \<host ip> ] [ -c \<config file path> ] [ -f \<fields> ] [ -a \<start time> ] [ -o \<stop time> ] [ request ] [ config ]
  
  ### Commands
  #### request
  Request performance data from the cnMaestro API. Requires either a valid config file, or at least a client id, client secret, and host ip. If a config file does not include a client id or client secret, a client id and secret can be passed in as options while the other config file values are used (useful if you don't want to save sensitive data).
  
  #### config
  Create a new config file, or overwrite an existing one. Prompts user for client id, client secret, host ip, fields, start time, and stop time. By default, new config files are created in the user's home directory.
    
  ### Options 
  #### -i or --client-id
  Takes a valid 16-digit client id. Option -i and option -s are mutually inclusive. Default: none
  
  #### -s or --client-secret
  Takes a valid 30-digit client secret. Option -s and option -i are mutually inclusive. Default: none
    
  #### -p or --host-ip
  Takes an ip address. Default: none
    
  #### option -c or --config-file
  Takes a file path. If the config argument is included and the file does not exist, it is created. If only a file name is passed, the program will look for the file within the user's home directory. Default: '~/config.json'
  
  #### -f or --fields
  Takes a string of fields to pull from the cnMaestro API. Field names must be separated by a comma, with no spaces. Default: 'name,timestamp,radio.dl_kbits,radio.ul_kbits'
     
  #### -a or --start-time
  Takes an integer, representing the first day to pull data from ( __ days ago @ T00:00:00-05:00). Default: 7, Max: 7
     
  #### -o or --stop-time
  Takes an integer, representing the last day to pull data from ( __ days ago @ T23:00:00-05:00). Default: 1, Max: 7
  
  #### --help
  Display the help menu
