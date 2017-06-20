import boto3
import json
import click
from .base import cli, get_instance, datetime_handler
from colorama import Fore, Style
from botocore.vendored.requests.exceptions import ConnectionError


@cli.command()
@click.pass_context
def list_tables(ctx):
    """List all tables of DynamoDB."""
    try:
        dynamodb = get_instance()

        tables = map(lambda x: x.name, dynamodb.tables.all())

        response = {
            "TableNames": tables
        }

        print(json.dumps(response, sort_keys=True, indent=4, default=datetime_handler))
    except ConnectionError as e:
        print(Fore.RED + "[!] ConnectionError: {}".format(e.message) + Style.RESET_ALL)
