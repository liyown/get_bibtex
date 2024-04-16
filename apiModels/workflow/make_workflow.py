import os

from tqdm import tqdm

from apiModels.meta_class import AbstractGetBibTex


class MakeWorkflow:
    def __init__(self, input_file_path, output_file_path, *args):
        self.raws = None
        self.api_models = []
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        if len(args) != 0:
            for arg in args:
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
        for api_model in self.api_models:
            api_model.isready()

    def running(self):
        self.isready()
        failed_results = self.raws
        for api_model in self.api_models:
            success_bibtexs, failed_results = api_model.get_bibtexs(failed_results)
            tqdm.write("find bibtex from {}: {}".format(api_model.__class__.__name__, len(success_bibtexs)))
            with open(self.output_file_path, "a", encoding='utf-8') as f:
                f.write("----------------------{} Result-----------------\n".format(api_model.__class__.__name__))
                for bibtex in success_bibtexs:
                    f.write(bibtex + "\n")
