#!/usr/bin/env python
# -*- coding: utf-8 -*-
import django
from django.core.mail import EmailMessage
from django.utils import timezone
from mr_csv_worker.error_tracer import print_error
from mr_csv_worker.worker import CsvWorker
from avtoresurs_new.settings import DEFAULT_FROM_EMAIL

import os
os.environ["DJANGO_SETTINGS_MODULE"] = "avtoresurs_new.settings"
django.setup()


PROTOCOL_REPORTS_EMAIL = 'shaman@born2fish.ru'

csv_worker = CsvWorker()


def send_bonus_error_protocol(protocol):
    """ :param protocol: is csv error bonuses protocol """
    try:
        email = EmailMessage (
            '[АВТОРЕСУРС] Бонусы, которые не получилось импортировать',
            '%s' % timezone.now(),
            DEFAULT_FROM_EMAIL,
            [PROTOCOL_REPORTS_EMAIL]
        )
        email.attach_file(protocol)
        email.send(fail_silently=False)
    except Exception as e:
        print(e)
        print_error()


def generate_protocol(path_to_file, error_rows):
    """
     :param path_to_file: full path to protocol file
     :param error_rows: this is the list of rows from
      bonuses csv file contains errors
      :return None or path to created protocol file
     """
    try:
        list_of_dict = []
        fields_names_list = ['error rows']
        for err_row in error_rows:
            list_of_dict.append({fields_names_list[0]: err_row})
        csv_worker.write_rows_from_list_of_dict(csv_file_path=path_to_file, fields_names_list=['error rows'],
                                                list_of_dict=list_of_dict)
        return path_to_file
    except Exception as e:
        print(e)
        return None


def import_bonuses(bonus_file_path, protocol_path=''):
    """ import bonuses from csv file """
    rows = csv_worker.get_rows_list_from_csv(csv_file_path=bonus_file_path, encoding='cp1251', delimiter=';')
    error_rows = []
    for row in rows:
        try:
            # try to get data from row
            item_code = row[0]
            item_name = row[1]
            item_bonus_price = row[2]
            # try to int price and generate report protocol on error
            try:
                int(item_bonus_price)
                print(item_code, item_name, item_bonus_price)
                # TODO write code below:
                # next we should create an object from this fields (django model) and save it, or return dict
            except ValueError:
                print("Wrong format in bonus row. This will be reported.")
                error_rows.append(row)

        except IndexError:
            error_rows.append(row)
            print("File '%s': wrong columns markup. This will be reported.\nrow=%s" % (bonus_file_path, row))

    if error_rows:
        protocol = generate_protocol(path_to_file=protocol_path, error_rows=error_rows)
        if protocol:
            send_bonus_error_protocol(protocol=protocol)
