# cnm-usage.py

import click
import json

@click.command()
@click.option(
    '--auth-data', '-a', 'dest'
    help='Client ID for the cnMaestro API',
)
def auth(dest):
    f = open(dest, 'r')
    client_id = f.json()['client_id']
    client_secret = f.json()['client_secret']

'''
def main():
    auth()


if __name__ == '__main__':
    main()
'''
