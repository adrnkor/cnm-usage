# cnm-usage
cli app to pull usage data from cnMaestro API.

## Usage

**CONFIG FILE OUT OF DATE ! I'll get around to that changing that...**

#### Currently works by directly calling the cli.py script.
   \> python cli.py \[ -i \<client id> ] \[ -s \<client secret> ] \[ -c \<config file path> ] \[ request ] \[ config ]
  
  ### arguments
  #### request
    takes an ip address. attempts to generate an api session.
  
  #### config
    takes no arguments. prompts for a client id and client secret, and creates or updates a config file. 
    
  ### options 
  #### option -i or --client-id
    takes a valid 16-digit client id. option -i and option -s are mutually inclusive.
  
  #### option -s or --client-secret
    takes a valid 30-digit client secret. option -s and option -i are mutually inclusive.
    
  #### option -c or --config-file
    takes a file path. if the config argument is included and the file does not exist, it is created. if the request argument is included and the -i and -s options     are not both set, the config file is used; if the -i and -s options are both set, the config file is not used. if the request argument is included and options
    -i, -s, and -c are not specified, the program will look for a config file at the default location ('./.auth.cfg')
