'''
    CLI for cnm_usage app
    example command:
        > python cli.py -i <client id> -s <client secret> request <host ip>
        -i LSaNKGIUtYfJO4Uq -s SDtBmkPPfx0C6CfBfMIbqYNM2p1C1z request 208.93.184.17
'''

import os
import sys
import click
import json
from cnm_usage import api
from datetime import datetime, timedelta

class ClientID(click.ParamType):
    name = 'client-id'
    '''
    def convert(self, value, param, ctx):
        found = re.match(r'[0-9a-f]{16}', value)

        if not found:
            self.fail(
                f'{value} is not a 16-character hexadecimal string',
                param,
                ctx,
            )

        return value
    '''

class ClientSecret(click.ParamType):
    name = 'client-secret'

    '''
    def convert(self, value, param, ctx):
        found = re.match(r'[0-9a-f]{30}', value)

        if not found:
            self.fail(
                f'{value} is not a 30-character hexadecimal string',
                param,
                ctx,
            )

        return value
    '''


class Fields(click.ParamType):
    name = 'fields'


class StartTime(click.ParamType):
    name = 'start'

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
    name = 'stop'

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
Define command options to pass client id, client secret, and a config file.
Options are optional, so the user can pass in either a client id and a client secret
or a config file name.
'''
@click.group()
@click.option(
    '--client-id', '-i',
    type=ClientID(),
    help='Client ID for the cnMaestro API',
)
@click.option(
    '--client-secret', '-s',
    type=ClientSecret(),
    help='Client secret for the cnMaestro API',
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
    help="Fields to pull from the cnMaestro API"
)
@click.option(
    '--start', '-a',
    type=StartTime(),
    default=7,
)
@click.option(
    '--stop', '-o',
    type=StopTime(),
    default=1,
)

@click.pass_context
def main(ctx, client_id, client_secret, config_file, fields, start, stop):
    """
    Start of program.
    Creates context object (ctx) from options or config file.
    """
    filename = os.path.expanduser(config_file)

    if os.path.exists(filename):
        if not (client_id and client_secret):
            with open(filename) as cfg:
                data = json.load(cfg)

                client_id = data['client_id']
                client_secret = data['client_secret']
                fields = data['params']['fields']
                start_time = data['params']['start_time']
                stop_time = data['params']['stop_time']
        else:
            print("{} exists, but a different client id and client secret was supplied.".format(filename))
            with open(filename) as cfg:
                data = json.load(cfg)

                fields = data['params']['fields']
                start_time = data['params']['start_time']
                stop_time = data['params']['stop_time']

    if not os.path.exists(filename):
        if not (client_id and client_secret):
            print("{} does not exist. Aborting...".format(filename))
            sys.exit()
        else:
            print("{} does not exist. A config file can be created.".format(filename))
            click.confirm("Do you want to continue?", abort=True)
            config = {
                        "client_id": client_id,
                        "client_secret": client_secret,
                        "params": {
                            "fields": fields,
                            "start_time": start,
                            "stop_time": stop,
                        }
                     }

            with open(filename, 'w') as cfg:
                json.dump(config, cfg)

    ctx.obj = {
        'client_id': client_id,
        'client_secret': client_secret,
        'config_file': filename,
        'fields': fields,
        'start_time': start_time,
        'stop_time': stop_time,
    }

@main.command()
@click.pass_context
def config(ctx):
    """
    Prompts user to enter client id and client secret, stores these values in a file.
    Filename defined by the --config-file option
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
                "params": {
                    "fields": fields,
                    "start_time": start_time,
                    "stop_time": stop_time,
                }
             }

    with open(config_file, 'w') as cfg:
        json.dump(config, cfg)
        #cfg.writelines([client_id, '\n'+client_secret])


@main.command()
@click.argument('host_ip')
@click.pass_context
def request(ctx, host_ip):
    """
    Generate and authenticate an API access token.
    """
    client_id = ctx.obj['client_id']
    client_secret = ctx.obj['client_secret']
    params = {'fields': ctx.obj['fields'], 'start_time': ctx.obj['start_time'], 'stop_time': ctx.obj['stop_time']}

    api_call = api.Call(host_ip, client_id, client_secret, params)
    api_call.getPerformance()
    # access_token = api.auth.generate_api_session(host_ip, client_id, client_secret)
    print("Nice!")


if __name__ == "__main__":
    main()
