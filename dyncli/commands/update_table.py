import click
import json
from .base import cli, get_instance, datetime_handler
from botocore.exceptions import ClientError
from botocore.vendored.requests.exceptions import ConnectionError
from colorama import Fore, Back, Style


@cli.command()
@click.option('-r', '--read-units', type=int, default=None, help='Read capacity units. (default: 1)')
@click.option('-w', '--write-units', type=int, default=None, help='Write capacity units. (default: 1)')
@click.argument('table_name', metavar='TABLE')
def update_table(read_units, write_units, table_name):
    """Modifies a table.

    Modifies a DynamoDB table with TABLE name.

    You can only perform one of the following operations at once:

        Modify the provisioned throughput settings of the table.

            -r/--read-units - read capacity units\n
            -w/--write-units - write capacity units
    """
    try:
        dynamodb = get_instance()

        table = dynamodb.Table(table_name)

        provisioned_throughput = {}

        if read_units:
            provisioned_throughput['ReadCapacityUnits'] = read_units
            provisioned_throughput['WriteCapacityUnits'] = table.provisioned_throughput['WriteCapacityUnits']

        if write_units:
            if not 'ReadCapacityUnits' in provisioned_throughput:
                provisioned_throughput['ReadCapacityUnits'] = table.provisioned_throughput['ReadCapacityUnits']
            provisioned_throughput['WriteCapacityUnits'] = write_units

        if provisioned_throughput:
            table.update(ProvisionedThroughput=provisioned_throughput)

        response = {
            "TableDescription": {
                "TableArn": table.table_arn,
                "AttributeDefinitions": table.attribute_definitions,
                "ProvisionedThroughput": table.provisioned_throughput,
                "TableSizeBytes": table.table_size_bytes,
                "TableName": table.table_name,
                "TableStatus": table.table_status,
                "KeySchema": table.key_schema,
                "ItemCount": table.item_count,
                "CreationDateTime": table.creation_date_time
            }
        }

        print(json.dumps(response, sort_keys=True, indent=4, default=datetime_handler))
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(Fore.RED + "[!] Table '{}' already exists".format(table_name) + Style.RESET_ALL)
        else:
            print(Fore.RED + "[!] {}: {}".format(e.response['Error']['Code'], e.response['Error']['Message']) + Style.RESET_ALL)
    except ConnectionError as e:
        print(Fore.RED + "[!] ConnectionError: {}".format(e.message) + Style.RESET_ALL)
