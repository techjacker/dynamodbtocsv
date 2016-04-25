from dynamodbtocsv import dynamodbtocsv
import os
import json
import unittest
# import pprint

fixts_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
fixts = {
    'input': 'unordered_rows.json',
    'output': 'ordered_rows.json'
}
fixts_json = {}
for k in fixts:
    with open(os.path.join(fixts_dir, fixts[k])) as fixt:
        fixts_json[k] = json.load(fixt)
        fixts[k] = fixt.read()


class TestOrderer(unittest.TestCase):
    def test_order_single_row(self):
        orderer = dynamodbtocsv.Orderer(
            order_file_name=''
            # order_file_name='tests/fixtures/ordered_rows.json'
        )
        # ordered_row = orderer.order_cols_in_row(fixts_json['input'][0])
        # self.assertEqual(ordered_row, fixts_json['output'][0])

    # def test_order_all_rows(self):
    #     orderer = dynamodbtocsv.Orderer(
    #         order_file_name='tests/fixtures/order_no_nicename.json'
    #     )
    #     ordered_rows = orderer.run(fixts_json['input'])
    #     self.assertEqual(ordered_rows, fixts_json['output'])


# class TestCSV(unittest.TestCase):
    # def test_writes_csv_cols_in_order(self):
    #     orderer = dynamodbtocsv.Orderer()
    #     writer = dynamodbtocsv.CSVWriter()

    #     ordered_rows_nicename = orderer.run(fixts_json['input'])
    #     writer.run(ordered_rows_nicename)

        # print('')
        # print('ordered_rows_nicename')
        # pprint.pprint(json.dumps(ordered_rows_nicename))
        # print('')
        # self.assertEqual(json.dumps(ordered_rows_nicename), fixts['output_nicename'])
