#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from avtoresurs_new.support.csv_support import CsvWorker


class CsvWorkerTest(unittest.TestCase):
    worker = CsvWorker()
    test_file_4_read = 'resources/test_bonus_source_file.csv'
    test_file_4_write = 'results/test.csv'

    def test_get_rows_list_from_csv(self):
        rows = self.worker.get_rows_list_from_csv(csv_file_path=self.test_file_4_read, encoding='cp1251',
                                                  start_row=1, end_row=2)
        self.assertIsNotNone(rows)
        self.assertEqual(len(rows), 1)

    def test_write_rows_from_dict(self):
        field_names = ['item code', 'item_name']
        list_to_print = [
            {field_names[0]: 'x150', field_names[1]: 'test item 1'},
            {field_names[0]: 'x250', field_names[1]: 'test item 2'},
            {field_names[0]: 'x350', field_names[1]: 'test item 3'},
        ]
        self.worker.write_rows_from_list_of_dict(csv_file_path=self.test_file_4_write, fields_names_list=field_names,
                                                 list_of_dict=list_to_print, print_header=True)
        ok_report_text = "'%s' file was wrote" % self.test_file_4_write
        self.assertEqual(self.worker.report, ok_report_text)

