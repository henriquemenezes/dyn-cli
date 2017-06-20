# dyn-cli

Command Line Interface for Dynamo DB

Content:

* [Installation](#installation)
* [Usage](#usage)
* [Commands](#commands)
  + [List tables](#list-tables)
  + [Create table](#create-table)
  + [Update table](#update-table)
  + [Delete table](#delete-table)
* [Examples](#examples)

## Installation

The easiest way to install dyn-cli is to use [pip](https://pip.pypa.io//en/latest/):

```bash
$ pip install dyncli
```

## Usage

Synopsis:

```bash
$ dyn [OPTIONS] COMMAND [ARGS]...
```

List of commands:

* [List tables](#list-tables)
* [Create table](#create-table)
* [Update table](#update-table)
* [Delete table](#delete-table)

### Options

You can configure your AWS credentials via options. The following table shows these options.

| Option                              | Description                                                                  |
|-------------------------------------|------------------------------------------------------------------------------|
| `-a`, `--access-key AWS_ACCESS_KEY` | AWS Access Key ID. (default: local)                                          |
| `-s`, `--secret-key AWS_SECRET_KEY` | AWS Secret Key. (default: local)                                             |
| `-r`, `--region AWS_REGION`         | AWS Region. (default: us-east-1)                                             |
| `-n`, `--no-local`                  | Disable local endpoint_url set up to http://localhost:8000. (default: false) |
| `-h`, `--help`                      | Show help message.                                                           |

## Commands

### List tables

List all tables of DynamoDB.

```bash
$ dyn list_tables
```

### Create table

Creates a DynamoDB table with `TABLE` name and attributes defined in `ATTRIBUTE`.

```bash
$ dyn create_table [OPTIONS] TABLE ATTRIBUTE [ATTRIBUTE]...
```

#### Options

| Option                              | Description                                                                  |
|-------------------------------------|------------------------------------------------------------------------------|
| `-r`, `--read-units INTEGER`        | Read capacity units. (default: 1)                                            |
| `-w`, `--write-units INTEGER`       | Write capacity units. (default: 1)                                           |

#### Atrributes

The `ATTRIBUTE` argument can be defined like: `name:type[:pk][:sk]`

* _name_ - name of attribute.
* _type_ - type of attribute that can be:
  + `s` - string
  + `n` - number
  + `b` - binary
* `pk` - first attribute of primary key (partition key - HASH)
* `sk` - second attribute of primary key (sort key - RANGE)

### Update table

Modifies a DynamoDB table with TABLE name.

```bash
$ dyn update_table [OPTIONS] TABLE
```

#### Options

| Option                              | Description                                                                  |
|-------------------------------------|------------------------------------------------------------------------------|
| `-r`, `--read-units INTEGER`        | Read capacity units. (default: 1)                                            |
| `-w`, `--write-units INTEGER`       | Write capacity units. (default: 1)                                           |

### Delete table

Deletes a table of DynamoDB.

```bash
$ dyn delete_table TABLE
```

## Examples

Listing all tables:

```bash
$ dyn list_tables
```

```json
{
    "TableNames": [
        "Movies",
        "Music"
    ]
}
```

Creating Music table:

```bash
$ dyn create_table Music Artist:s:pk SongTitle:s:sk
```

```json
{
    "TableDescription": {
        "AttributeDefinitions": [
            {
                "AttributeName": "Artist",
                "AttributeType": "S"
            },
            {
                "AttributeName": "SongTitle",
                "AttributeType": "S"
            }
        ],
        "CreationDateTime": "2017-07-02T23:19:52.932000-03:00",
        "ItemCount": 0,
        "KeySchema": [
            {
                "AttributeName": "Artist",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "SongTitle",
                "KeyType": "RANGE"
            }
        ],
        "ProvisionedThroughput": {
            "LastDecreaseDateTime": "1969-12-31T21:00:00-03:00",
            "LastIncreaseDateTime": "1969-12-31T21:00:00-03:00",
            "NumberOfDecreasesToday": 0,
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1
        },
        "TableArn": "arn:aws:dynamodb:ddblocal:000000000000:table/Music",
        "TableName": "Music",
        "TableSizeBytes": 0,
        "TableStatus": "ACTIVE"
    }
}
```

Updating Music table:

```bash
$ dyn update_table Music -r 10 -w 10
```

```javascript
{
    "TableDescription": {
        "AttributeDefinitions": [
            {
                "AttributeName": "Artist",
                "AttributeType": "S"
            },
            {
                "AttributeName": "SongTitle",
                "AttributeType": "S"
            }
        ],
        "CreationDateTime": "2017-07-02T23:19:52.932000-03:00",
        "ItemCount": 0,
        "KeySchema": [
            {
                "AttributeName": "Artist",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "SongTitle",
                "KeyType": "RANGE"
            }
        ],
        "ProvisionedThroughput": {
            "LastDecreaseDateTime": "1969-12-31T21:00:00-03:00",
            "LastIncreaseDateTime": "1969-12-31T21:00:00-03:00",
            "NumberOfDecreasesToday": 0,
            "ReadCapacityUnits": 10,
            "WriteCapacityUnits": 10
        },
        "TableArn": "arn:aws:dynamodb:ddblocal:000000000000:table/Music",
        "TableName": "Music",
        "TableSizeBytes": 0,
        "TableStatus": "ACTIVE"
    }
}
```

Deleting Music table:

```bash
$ dyn delete_table Music
```

```json
{
    "TableDescription": {
        "ItemCount": 0,
        "ProvisionedThroughput": {
            "LastDecreaseDateTime": "1969-12-31T21:00:00-03:00",
            "LastIncreaseDateTime": "1969-12-31T21:00:00-03:00",
            "NumberOfDecreasesToday": 0,
            "ReadCapacityUnits": 10,
            "WriteCapacityUnits": 10
        },
        "TableArn": "arn:aws:dynamodb:ddblocal:000000000000:table/Music",
        "TableName": "Music",
        "TableSizeBytes": 0,
        "TableStatus": "DELETING"
    }
}
```
