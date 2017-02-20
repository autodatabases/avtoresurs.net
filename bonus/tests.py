from django.test import TestCase
import unittest

# Create your tests here.
from avtoresurs_new.settings import UNIT_TEST_FOLDER
from bonus.bonus_importer import import_bonuses


class BonusImporterTest(unittest.TestCase):

    def test_import_bonuses(self):
        bonus_file_path = '%s%s' % (UNIT_TEST_FOLDER, 'resources/test_bonus_source_file.csv')
        protocol_path = '%s%s' % (UNIT_TEST_FOLDER, 'results/test_bonus_protocol.csv')
        import_bonuses(bonus_file_path=bonus_file_path, protocol_path=protocol_path)
