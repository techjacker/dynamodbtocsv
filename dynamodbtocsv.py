#!/usr/bin/env python3

import boto3
import json
import os
import csv
import argparse
import pprint
from collections import OrderedDict


class Exporter:
    def __init__(self, row_limit, profile_name):
        self.row_limit = row_limit
        if profile_name != '':
            boto3.setup_default_session(profile_name=profile_name)
        self.client = boto3.client('dynamodb')
        self.resource = boto3.resource('dynamodb')

    def get_rows(self, table_name, rows=[], last_evaluated_key=None):
        response = self.client.scan(
            TableName=table_name,
            Limit=self.row_limit,
            **({"ExclusiveStartKey": last_evaluated_key}
                if last_evaluated_key else {})
        )

        rows = rows + response['Items']

        # for testing recursion on small tables (< 10000 (default) rows)
        # if 'LastEvaluatedKey' in response and len(rows) < 100000000000:
        if 'LastEvaluatedKey' in response and len(rows) < self.row_limit:
            return rows, response['LastEvaluatedKey']
        else:
            return rows, None


class Orderer():
    def __init__(self, order_file_name=''):
        if order_file_name != '':
            print('')
            print('order_file_name')
            pprint.pprint(order_file_name)
            print('')
            file_path = os.path.join(os.getcwd(), order_file_name)
            if os.path.isfile(file_path):
                with open(file_path) as order_file:
                    self.order = json.load(order_file)

    def order_cols_in_row(self, row):
        ordered_row = OrderedDict()
        for item in self.order:
            remove_content = 'remove_content' in item and \
                item['remove_content'] is True
            col = {}
            col[item['nicename']] = row[item['name']]['S'] \
                if item['name'] in row and \
                remove_content is not True \
                else ''
            ordered_row.update(col)
        return ordered_row

    def run(self, rows):
        if self.order != '':
            ordered_rows = []
            for row in rows:
                ordered_rows.append(self.order_cols_in_row(row))
            return ordered_rows
        else:
            return rows


class CSVWriter():
    def __init__(self, export_file_name='table.csv'):
        self.file_path = os.path.join(os.getcwd(), export_file_name)

    def run(self, rows):
        with open(self.file_path, 'w') as f:
            writer = csv.DictWriter(f, rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)


class DBtoCSV():
    def __init__(
        self,
        row_limit,
        order_file_name,
        profile_name,
        export_file_name
    ):
        self.exporter = Exporter(row_limit, profile_name)
        self.orderer = Orderer(order_file_name)
        self.writer = CSVWriter(export_file_name)

    def run(self, table_name, rows=[], last_evaluated_key=None):

        rows, last_evaluated_key = self.exporter.get_rows(
            table_name=table_name,
            rows=rows,
            last_evaluated_key=last_evaluated_key
        )

        if last_evaluated_key is not None:
            print('got %d rows...' % len(rows))
            self.run(
                table_name=table_name,
                rows=rows,
                last_evaluated_key=last_evaluated_key
            )
        else:
            rows = self.orderer.run(rows)
            self.writer.run(rows)
            print('COMPLETE!\nTotal rows: %d\nCSV written to: %s' %
                  (len(rows), self.writer.file_path)
                  )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='DynamoDB to CSV',
        epilog='eg:./dynamodbtocsv.py your-dynamodb-table'
    )
    parser.add_argument('table_name', help='the DynamoDB table name')
    parser.add_argument('-l', '--limit', type=int, help='row limit (default=10000)', default=10000)
    parser.add_argument('-e', '--export', type=str, help='name of CSV to write to (default=table.csv)', default='table.csv')
    parser.add_argument('-o', '--order', type=str, help='order config filename')
    parser.add_argument('-p', '--profile', type=str, help='AWS profile to use')
    args = parser.parse_args()

    dbtocsv = DBtoCSV(
        row_limit=args.limit,
        order_file_name=args.order,
        profile_name=args.profile,
        export_file_name=args.export
    )
    dbtocsv.run(
        table_name=args.table_name
    )
