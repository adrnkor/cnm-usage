'''
    CLI for cnm-usage app
    example command:
        > python cli.py -i <client id> -s <client secret> request <host ip>
'''

import re
import os
import click
import requests

import auth

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
    default='./.auth.cfg',
)

@click.pass_context
def main(ctx, client_id, client_secret, config_file):
    """
    Start of program.
    Creates context object (ctx) from options or config file.
    """
    filename = os.path.expanduser(config_file)

    if not (client_id or client_secret) and os.path.exists(filename):
        with open(filename) as cfg:
            client_id = cfg.readline()
            client_secret = cfg.readline()

    ctx.obj = {
        'client_id': client_id,
        'client_secret': client_secret,
        'config_file': filename,
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

    with open(config_file, 'w') as cfg:
        cfg.writelines([client_id, '\n'+client_secret])


@main.command()
@click.argument('host_ip')
@click.pass_context
def request(ctx, host_ip):
    """
    Generate and authenticate an API access token.
    """
    client_id = ctx.obj['client_id']
    client_secret = ctx.obj['client_secret']

    access_token = auth.generate_api_session(host_ip, client_id, client_secret)
    print(f"Nice!")


if __name__ == "__main__":
    main()
