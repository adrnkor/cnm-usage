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

@click.group()
@click.option(
    '--client-id', '-i',
    type=ClientID(),
    help='Client ID for the cnMaestro API',
)
@click.option(
    '--client-secret', '-s',
    type=ClientSecret(),
    help='Client secret key for the cnMaestro API',
)
@click.option(
    '--config-file', '-c',
    type=click.Path(),
    default='./auth.cfg',
)
@click.pass_context
def main(ctx, client_id, client_secret, config_file):
    """
    A little weather tool that shows you the current weather in a LOCATION of
    your choice. Provide the city name and optionally a two-digit country code.
    Here are two examples:
    1. London,UK
    2. Canmore
    You need a valid API key from OpenWeatherMap for the tool to work. You can
    sign up for a free account at https://openweathermap.org/appid.
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
    Store configuration values in a file, e.g. the API key for OpenWeatherMap.
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
    Show the current weather for a location using OpenWeatherMap data.
    """
    client_id = ctx.obj['client_id']
    client_secret = ctx.obj['client_secret']

    access_token = auth.generate_api_session(host_ip, client_id, client_secret)
    print(f"Nice!")


if __name__ == "__main__":
    main()
