import unittest
from unittest import TestCase


class TestApiModels(TestCase):

    def setUp(self):
        self.raws = [
            "CBAM: Convolutional Block Attention Module",
            "A Comprehensive Survey on Graph Neural Networks",
            "Graph Attention Networks",
            "Graph Convolutional Networks for Text Classification",
            "attention is all you need",
            "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"
        ]

    def test_get_bibtex_from_dblp(self):
        from apiModels.get_bibtex_from_dblp import GetBibTexFromDBLP
        get_bibtex_from_dblp = GetBibTexFromDBLP()
        res = get_bibtex_from_dblp.get_bibtexs(self.raws)
        print(res)

    def test_get_bibtex_from_crossref(self):
        from apiModels.get_bibtex_from_crossref import GetBibTex
        get_bibtex_from_crossref = GetBibTex("1536727925@qq.com")
        res = get_bibtex_from_crossref.get_bibtexs(self.raws)
        print(res)

    @unittest.skip("Not api key provided")
    def test_get_bibtex_from_google_scholar(self):
        from apiModels.get_bibtex_from_google_scholar import GetBibTexFromGoogleScholar
        google_scholar_api_key = "api_key"
        get_bibtex_from_google_scholar = GetBibTexFromGoogleScholar(google_scholar_api_key,
                                                                    GetBibTexFromGoogleScholar.APA)
        self.assertEqual(get_bibtex_from_google_scholar.get_bibtexs(self.raws), ([], []))

    def test_crossref2dblp(self):
        from apiModels.workflow.crossref2dblp import Crossref2Dblp
        from apiModels.get_bibtex_from_google_scholar import GetBibTexFromGoogleScholar
        get_bibtex_from_google_scholar = GetBibTexFromGoogleScholar(api_key="api")
        crossref2dblp = Crossref2Dblp("1536727925@qq.com", "inputfile/Bibliographyraw.txt",
                                      "outputfile/Bibliography.txt", get_bibtex_from_google_scholar)
        crossref2dblp.running()
        self.assertTrue(True)

    def test_make_workflow(self):
        from apiModels.workflow.make_workflow import MakeWorkflow
        from apiModels.get_bibtex_from_google_scholar import GetBibTexFromGoogleScholar
        from apiModels.get_bibtex_from_crossref import GetBibTex

        get_bibtex_from_google_scholar = GetBibTexFromGoogleScholar(api_key="api")
        get_bibtex_from_crossref = GetBibTex("1536727925@qq.com")
        make_workflow = MakeWorkflow("inputfile/Bibliographyraw.txt", "outputfile/Bibliography.txt",
                                     get_bibtex_from_google_scholar, get_bibtex_from_crossref)
        make_workflow.running()
        self.assertTrue(True)
