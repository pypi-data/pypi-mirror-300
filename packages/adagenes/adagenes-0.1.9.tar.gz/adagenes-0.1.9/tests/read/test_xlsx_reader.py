import unittest, os
import adagenes


class TestXLSXReader(unittest.TestCase):

    def test_excel_reader(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        genome_version = 'hg19'


