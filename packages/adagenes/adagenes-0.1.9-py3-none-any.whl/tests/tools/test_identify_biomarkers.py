import unittest
import adagenes as av


class TestIdentifyBiomarkers(unittest.TestCase):

    def test_identify_biomarkers(self):
        data = {"TP53":{}, "chr7:140753336A>T":{}, "BRAF:p.V600E":{}, "CRTAP:c.320_321del": {}}
        bframe= av.BiomarkerFrame(data,genome_version="hg38")
        bframe = av.tools.identify_biomarkers(bframe)
        print(bframe.data)
        self.assertEqual(list(bframe.data.keys()),["TP53","chr7:140753336A>T","BRAF:V600E", "CRTAP:c.320_321del"],"")
        self.assertEqual(bframe.data["CRTAP:c.320_321del"]["mutation_type"],"indel","")
