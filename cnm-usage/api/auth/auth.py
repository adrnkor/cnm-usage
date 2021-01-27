# cnMaestro sample API test code
# reworked by Sal K (Dec 2020/Jan 2021)

# "API test code for cnMaestro that demonstrates session establishment and API
# api. The client connects to cnMaestro using the Client Id and Client
# Secret downloaded from the Client API page in the cnMaestro UI. The Client
# receives a URL, Access Token, and Expiration Interval (in seconds)
# defining how long the token is valid. The URL and Access Token are used
# for subsequent API requests." -- cnMaestro 2.4.1 RESTful API documentation

import sys
import requests
import json
import base64
from datetime import datetime, timedelta

# LIVE: 208.93.184.19
# TEST: 208.93.184.17
# TEST CREDS: (ID) LSaNKGIUtYfJO4Uq (SECRET) SDtBmkPPfx0C6CfBfMIbqYNM2p1C1z

HOST = '208.93.184.19'
CLIENT_ID = 'BKKKzPEYA6n3KtOJ'
CLIENT_SECRET = '37kxAfdfcnPkE7UitBNLRoKgB0cY13'

def check_http_return(section, url, code, request):
    if int(code) != 200:
        print('{0} failed with HTTP status {1}'.format(section, code))
        print('URL: {}'.format(url))
        try:
            print(json.dumps(request.json(), indent=2))
        except: pass
        sys.exit(1)

# Retrieve access parameters (url, access_token, and expires_in).
def get_access_parameters(host, client_id, client_secret):
    token_url = 'https://{}/api/v1/access/token'.format(host)
    encoded_credentials = base64.b64encode('{}:{}'.format(client_id, client_secret).encode()).decode()
    headers = {
        'Authorization': 'Basic {}'.format(encoded_credentials),
        'Content-Type':'application/x-www-form-urlencoded'
    }
    print(encoded_credentials)
    body = 'grant_type=client_credentials'
    r = requests.post(token_url, body, headers=headers, verify=False)
    check_http_return('Access Parameters', token_url, r.status_code, r)
    return r.json()['access_token'], r.json()['expires_in']

# Validate the expiration of the access token.
def validate_access_token(host, access_token):
    validate_url = 'https://{}/api/v1/access/validate_token'.format(host)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
    }
    r = requests.get(validate_url, headers=headers, verify=False)
    check_http_return('Validate Access Token', validate_url, r.status_code, r)
    return r.json()['expires_in']

def generate_api_session(host, client_id, client_secret):
    # Retrieve access parameters and generate API session
    print('\nRetrieve Access Parameters')
    access_token, expires_in = get_access_parameters(host, client_id, client_secret)
    print('Success: access_token ({}) expires_in ({})\n'.format(access_token, expires_in))


    # Validate time remaining for the access token
    print('Validating expiration time')
    expires_in_check = validate_access_token(host, access_token)
    print('Success: expiresIn ({})\n'.format(expires_in_check))
    return access_token

# Execute API using URL returned in access parameters.
def call_api(host, path, access_token):
    api_url = 'https://{}{}'.format(host, path)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
    }
    r = requests.get(api_url, headers=headers, verify=False)
    check_http_return("API", api_url, r.status_code, r)
    return r.json()
