import unittest, os
import adagenes


class TestCSVReader(unittest.TestCase):

    def test_csv_reader(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        genome_version = 'hg19'

        infile = __location__ + "/../test_files/somaticMutations.ln50.revel.csv"
        bframe = adagenes.read_file(infile, genome_version=genome_version)
        print(list(bframe.data.keys())[0])
        print(bframe)

        self.assertEqual("chr7:21744592insG",list(bframe.data.keys())[0],"")
        self.assertEqual("7", bframe.data["chr7:21744592insG"]["variant_data"]["CHROM"], "")

        self.assertEqual("chr7:21744592insG", list(bframe.data.keys())[0], "")
        self.assertEqual("7", bframe.data["chr7:92029936A>G"]["variant_data"]["CHROM"], "")


