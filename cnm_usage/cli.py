'''
    CLI for cnm_usage app
    example command:
        > python cli.py -i <client id> -s <client secret> request <host ip>
        -i LSaNKGIUtYfJO4Uq -s SDtBmkPPfx0C6CfBfMIbqYNM2p1C1z request 208.93.184.17
'''

import os
import sys
import re
import click
import json
from cnm_usage import api
from datetime import datetime, timedelta

class ClientId(click.ParamType):
    name = 'client-id'

    def convert(self, value, param, ctx):
        found = re.match(r'[0-9a-zA-Z]{16}', value)

        if not found:
            self.fail(
                f'{value} is not a valid client ID',
                param,
                ctx,
            )

        return value


class ClientSecret(click.ParamType):
    name = 'client-secret'

    def convert(self, value, param, ctx):
        found = re.match(r'[0-9a-zA-Z]{30}', value)

        if not found:
            self.fail(
                f'{value} is not a valid client secret',
                param,
                ctx,
            )

        return value


class Fields(click.ParamType):
    name = 'fields'


class StartTime(click.ParamType):
    name = 'start_time'

    def convert(self, value, param, ctx):
        try:
            v = int(value)
            if v <= 7:
                return (datetime.now() - timedelta(int(value))).strftime('%Y-%m-%d') + 'T00:00:00-05:00'
            else:
                raise ValueError(f"{value!r} is not a valid integer. start time must be less than 7 days ago")

        except TypeError:
            self.fail(
                "expected string for int() conversion, got "
                f"{value!r} of type {type(value).__name__}",
                param,
                ctx,
            )

        except ValueError:
            self.fail(f"{value!r} is not a valid integer", param, ctx)


class StopTime(click.ParamType):
    name = 'stop_time'

    def convert(self, value, param, ctx):
        try:
            v = int(value)
            if v <= 7:
                return (datetime.now() - timedelta(int(value))).strftime('%Y-%mw-%d') + 'T23:00:00-05:00'
            else:
                raise ValueError(f"{value!r} is not a valid integer. stop time must be less than 7 days ago")

        except TypeError:
            self.fail(
                "expected string for int() conversion, got "
                f"{value!r} of type {type(value).__name__}",
                param,
                ctx,
            )

        except ValueError:
            self.fail(f"{value!r} is not a valid integer", param, ctx)


'''
Define command options to pass in values. client-id, client_secret, and host_ip do not have default values and must either
be passed in through the command line or found in a specified config file.
'''
@click.group()
@click.option(
    '--client-id', '-i',
    type=ClientId(),
    help='Client ID for the cnMaestro API.',
)
@click.option(
    '--client-secret', '-s',
    type=ClientSecret(),
    help='Client secret for the cnMaestro API.',
)
@click.option(
    '--host-ip', '-p',
    type=str,
    help='Host IP to call the API.',
)
@click.option(
    '--config-file', '-c',
    type=click.Path(),
    default='~/config.json',
    help="Specify config file to read from. Default: ~/config.json"
)
@click.option(
    '--fields', '-f',
    type=str,
    default='name,timestamp,radio.dl_kbits,radio.ul_kbits',
    help="Fields to pull from the cnMaestro API. Field names must be separated by a comma, with no spaces."
)
@click.option(
    '--start-date', '-a',
    type=StartTime(),
    default=7,
    help="First day to pull data from ( __ days ago @ T00:00:00-05:00). Default: 7, Max: 7"
)
@click.option(
    '--stop-date', '-o',
    type=StopTime(),
    default=1,
    help="Last day to pull data from ( __ days ago @ T23:00:00-05:00). Default: 1, Max: 7"
)

@click.pass_context
def main(ctx, client_id, client_secret, host_ip, config_file, fields, start_time, stop_time):
    """
    Program to pull usage/performance data from the cnMaestro API. Pulls a maximum of 100 entries per call, within a time window starting at most one week ago."
    Note: Full functionality from the command line is not supported. The code will need to be edited directly to change some settings, such as request limits and offsets. This program should be further developed before it is used.
    """
    filename = os.path.expanduser(config_file)

    if os.path.exists(filename):
        if not host_ip:
            with open(filename) as cfg:
                data = json.load(cfg)
                host_ip = data['host_ip']

        if not (client_id and client_secret):
            with open(filename) as cfg:
                data = json.load(cfg)

                client_id = data['client_id']
                client_secret = data['client_secret']
                fields = data['params']['fields']
                start_time = data['params']['start_time']
                stop_time = data['params']['stop_time']

        else:
            print("{} exists, but a different client id and client secret was supplied. Using the ones supplied...".format(filename))
            with open(filename) as cfg:
                data = json.load(cfg)

                fields = data['params']['fields']
                start_time = data['params']['start_time']
                stop_time = data['params']['stop_time']

    if not os.path.exists(filename):
        if not (client_id and client_secret and host_ip):
            print("{} does not exist, and necessary input was not supplied. Aborting...".format(filename))
            sys.exit()
        else:
            print("{} does not exist. A config file can be created from the information given.".format(filename))
            click.confirm("Do you want to continue?", abort=True)
            config = {
                        "client_id": client_id,
                        "client_secret": client_secret,
                        "host_ip": host_ip,
                        "params": {
                            "fields": fields,
                            "start_time": start_time,
                            "stop_time": stop_time,
                        }
                     }

            with open(filename, 'w') as cfg:
                json.dump(config, cfg)

    ctx.obj = {
        'client_id': client_id,
        'client_secret': client_secret,
        'host_ip': host_ip,
        'config_file': filename,
        'fields': fields,
        'start_time': start_time,
        'stop_time': stop_time,
    }

@main.command()
@click.pass_context
def config(ctx):
    """
    Create a new config file, or overwrite an existing one. File path defined by --config-file PATH
    To skip a setting and have it be set as the default option, press Return.
    """
    config_file = ctx.obj['config_file']

    client_id = click.prompt(
        "Please enter your Client ID",
        default=ctx.obj.get('client_id', '')
    )
    client_secret = click.prompt(
        "Please enter your Client Secret",
        default=ctx.obj.get('client_secret', '')
    )
    host_ip = click.prompt(
        "Please enter the host IP",
        default=ctx.obj.get('host_ip', '')
    )
    fields = click.prompt(
        "Please enter the fields to retrieve",
        default=ctx.obj.get('fields', '')
    )
    start_time = click.prompt(
        "Please enter the start time",
        default=ctx.obj.get('start_time', '')
    )
    stop_time = click.prompt(
        "Please enter the stop time",
        default=ctx.obj.get('stop_time', '')
    )

    config = {
                "client_id": client_id,
                "client_secret": client_secret,
                "host_ip": host_ip,
                "params": {
                    "fields": fields,
                    "start_time": start_time,
                    "stop_time": stop_time,
                }
             }

    with open(config_file, 'w') as cfg:
        json.dump(config, cfg)


@main.command()
@click.pass_context
def request(ctx):
    """
    Request performance data from the cnMaestro API. Generates and authenticates an API access token, calls the API, then prints the json response.
    """

    # Set variables necessary for making an API call
    client_id = ctx.obj['client_id']
    client_secret = ctx.obj['client_secret']
    host_ip = ctx.obj['host_ip']
    params = {'fields': ctx.obj['fields'], 'start_time': ctx.obj['start_time'], 'stop_time': ctx.obj['stop_time']}

    # Create the API Call object
    api_call = api.Call(host_ip, client_id, client_secret, params)

    # Call the API
    call_response_perf = api_call.getPerformance()
    # call_response_dev = api_call.getDevices()

    print(call_response_perf)
    # print(call_response_devices)


if __name__ == "__main__":
    main()