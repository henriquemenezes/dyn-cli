import click
import boto3
import json
from .base import cli, get_attr_type, get_instance, datetime_handler
from botocore.exceptions import ClientError
from botocore.vendored.requests.exceptions import ConnectionError
from colorama import Fore, Back, Style


@cli.command()
@click.option('-r', '--read-units', default=1, help='Read capacity units. (default: 1)')
@click.option('-w', '--write-units', default=1, help='Write capacity units. (default: 1)')
@click.argument('table_name', metavar='TABLE')
@click.argument('attributes', nargs=-1, required=True, metavar='ATTRIBUTE [ATTRIBUTE]...')
def create_table(read_units, write_units, table_name, attributes):
    """Creates a table.

    Creates a DynamoDB table with TABLE name and attributes defined in ATTRIBUTE.

    The ATTRIBUTE argument can be defined like: name:type[:pk][:sk]

        name - name of attribute.\n
        type - type of attribute that can be:\n
            s - string\n
            n - number\n
            b - binary\n
        pk - first attribute of primary key (partition key - HASH)\n
        sk - second attribute of primary key (sort key - RANGE)\n
    """
    key_schema = []
    attributes_definitions = []
    provisioned_throughput = {
        'ReadCapacityUnits': read_units,
        'WriteCapacityUnits': write_units
    }

    for attr in attributes:
        values = attr.split(":")
        name = values[0]
        type_ = (get_attr_type(values[1]) if len(values) > 1 else 'S')
        pk = 'pk' in values
        sk = 'sk' in values

        attributes_definitions.append({
            'AttributeName': name,
            'AttributeType': type_
        })

        if pk:
            key_schema.append({
                'AttributeName': name,
                'KeyType': 'HASH'
            })

        if sk:
            key_schema.append({
                'AttributeName': name,
                'KeyType': 'RANGE'
            })

    try:
        dynamodb = get_instance()

        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attributes_definitions,
            ProvisionedThroughput=provisioned_throughput
        )

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
