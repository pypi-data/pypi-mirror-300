import unittest, os
import adagenes


class TestVCFReader(unittest.TestCase):

    def test_vcf_reader(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        genome_version = 'hg19'

        infile = __location__ + "/../test_files/somaticMutations.ln_4.vcf"
        bframe = adagenes.read_file(infile, genome_version=genome_version)
        print(list(bframe.data.keys())[0])
        print(bframe)

        self.assertEqual("chr12:25245350C>T",list(bframe.data.keys())[0],"")
        self.assertEqual("12", bframe.data["chr12:25245350C>T"]["variant_data"]["CHROM"], "")

        self.assertEqual("chr12:25245350C>T", list(bframe.data.keys())[0], "")
        self.assertEqual("12", bframe.data["chr12:25245350C>T"]["variant_data"]["CHROM"], "")

        self.assertEqual("chr12:25245350C>T", list(bframe.data.keys())[0], "")
        self.assertEqual("25245350", bframe.data["chr12:25245350C>T"]["variant_data"]["POS_hg19"], "")

        self.assertEqual("snv", bframe.data["chr12:25245350C>T"]["mutation_type"], "")
