import click
import botocore
import boto3
import datetime


__config = {}

@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-a', '--access-key', metavar='AWS_ACCESS_KEY', default='local', help='AWS Access Key ID. (default: local)')
@click.option('-s', '--secret-key', metavar='AWS_SECRET_KEY', default='local', help='AWS Secret Key. (default: local)')
@click.option('-r', '--region', metavar='AWS_REGION', default='us-east-1', help='AWS Region. (default: us-east-1)')
@click.option('-n', '--no-local', is_flag=True, help='Disable local endpoint_url set up to http://localhost:8000. (default: false)')
def cli(access_key, secret_key, region, no_local):
    __config['aws_access_key_id'] = access_key
    __config['aws_secret_access_key'] = secret_key
    __config['region_name'] = region

    if not no_local:
        __config['endpoint_url'] = 'http://localhost:8000'

def run():
    cli()

def get_attr_type(x):
    return (x.upper() if x in ['s', 'n', 'b'] else 'S')

def get_instance():
    dynamodb = boto3.resource('dynamodb', **__config)
    return dynamodb

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError
