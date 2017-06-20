import click
import boto3
import json
from .base import cli, get_instance, datetime_handler
from colorama import Fore, Style
from botocore.exceptions import ClientError
from botocore.vendored.requests.exceptions import ConnectionError


@cli.command()
@click.argument('table_name', metavar='TABLE')
def delete_table(table_name):
    """Deletes a table of DynamoDB."""
    try:
        dynamodb = get_instance()

        table = dynamodb.Table(table_name)

        response = {
            "TableDescription": {
                "TableArn": table.table_arn,
                "ProvisionedThroughput": table.provisioned_throughput,
                "TableSizeBytes": table.table_size_bytes,
                "TableName": table.table_name,
                "TableStatus": "DELETING",
                "ItemCount": table.item_count
            }
        }

        table.delete()

        print(json.dumps(response, sort_keys=True, indent=4, default=datetime_handler))
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(Fore.RED + "[!] Table '{}' doesn't exists".format(table_name) + Style.RESET_ALL)
        else:
            print(Fore.RED + "[!] {}: {}".format(e.response['Error']['Code'], e.response['Error']['Message']) + Style.RESET_ALL)
    except ConnectionError as e:
        print(Fore.RED + "[!] ConnectionError: {}".format(e.message) + Style.RESET_ALL)
