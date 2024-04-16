import os

from tqdm import tqdm

from apiModels.get_bibtex_from_crossref import GetBibTex
from apiModels.get_bibtex_from_dblp import GetBibTexFromDBLP
from apiModels.meta_class import AbstractGetBibTex


class Crossref2Dblp:
    """
    Get bibtex from crossref and dblp
    """

    def __init__(self, email, input_file_path, output_file_path, *args) -> None:
        self.raws = None
        self.crossref = GetBibTex(email)
        self.dblp = GetBibTexFromDBLP()
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        if len(args) != 0:
            for arg in args:
                self.api_models = []
                # 判断是否为AbstractGetBibTex的子类
                if not isinstance(arg, AbstractGetBibTex):
                    raise ValueError(f"args must be instance of AbstractGetBibTex, but got {type(arg)}")
                self.api_models.append(arg)

    def isready(self):
        # check if the input file exists if not create it
        if not os.path.exists(self.input_file_path):
            raise FileNotFoundError(f"Input file {self.input_file_path} not found")
        # check if the output file exists if not create it
        if not os.path.exists(self.output_file_path):
            raise FileNotFoundError(f"Output file {self.output_file_path} not found")
        # read the input file
        with open(self.input_file_path, "r", encoding='utf-8') as f:
            self.raws = f.readlines()
        # 判断API是否可用
        self.crossref.isready()
        self.dblp.isready()
        if hasattr(self, "api_models"):
            for api_model in self.api_models:
                api_model.isready()

    def running(self):
        self.isready()
        # get bibtex from CrossRef and failed search results
        success_bibtexs_crossref, failed_results = self.crossref.get_bibtexs(self.raws)

        # get bibtex from dbpl
        success_bibtexs_DBLP, failed_results = self.dblp.get_bibtexs(failed_results)

        with open(self.output_file_path, "w", encoding='utf-8') as f:
            f.write("----------------------Crossref Rasult-----------------\n")
            for bibtex in success_bibtexs_crossref:
                f.write(bibtex + "\n")
            f.write("----------------------DBLP Result-----------------\n")
            for bibtex in success_bibtexs_DBLP:
                f.write("[DBLP] " + bibtex + "\n")

        tqdm.write("find bibtex from CrossRef: " + str(len(success_bibtexs_crossref)))
        tqdm.write("find bibtex from DBLP: " + str(len(success_bibtexs_DBLP)))

        if hasattr(self, "api_models"):
            res = {}
            for api_model in self.api_models:
                success_bibtexs, failed_results = api_model.get_bibtexs(failed_results)
                res[api_model.__class__.__name__] = success_bibtexs

            with open(self.output_file_path, "a", encoding='utf-8') as f:
                f.write("----------------------[your Models Result]-----------------\n")
                for key, value in res.items():
                    f.write(f"-------------------{key} Result------------------------\n")
                    tqdm.write(f"{key} find bibtex: {len(value)}")
                    for bibtex in value:
                        f.write(bibtex + "\n")
                    f.write("\n")

        with open(self.output_file_path, "a", encoding='utf-8') as f:
            f.write("----------------------Not Found-----------------\n")
            for result in failed_results:
                f.write(result + "\n")
