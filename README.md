[![Build Status](https://travis-ci.org/techjacker/dynamodbtocsv.svg?branch=master)](https://travis-ci.org/techjacker/dynamodbtocsv)

# dynamodbtocsv

- Downloads a AWS DynamoDB table and exports to CSV
- Optionally pass a JSON config that specifies column order in CSV
- JSON config also allows column headings to be renamed in CSV
- requires python 3


## Usage

```Shell
$ ./dynamodbtocsv.py -h

usage: dynamodbtocsv.py [-h] [-l LIMIT] [-e EXPORT] [-o ORDER] [-p PROFILE]
                        table_name

DynamoDB to CSV

positional arguments:
  table_name            the DynamoDB table name

optional arguments:
  -h, --help            show this help message and exit
  -l LIMIT, --limit LIMIT
                        row limit (default=10000)
  -e EXPORT, --export EXPORT
                        name of CSV to write to (default=table.csv)
  -o ORDER, --order ORDER
                        order config filename
  -p PROFILE, --profile PROFILE
                        AWS profile to use
```



### Example Order JSON config
```JSON
[
    {"name": "dnyamoDB_col_3", "nicename": "New heading name of column 3 which is now the first column of our CSV"},
    {"name": "col_one"},
    {"name": "col_four", "remove_content": true, "nicename": "the content of these rows will be removed (they will be blank cells)"},
    {"name": "col_two", "nicename": "We will change the name of this column too and it will be placed as the 3rd column"}
]
```



## Development
```Shell
pyenv virtualenv 3.5.1 dynamodbtocsv
pyenv local dynamodbtocsv
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Tests
```Shell
nostests
```
