import re

from gradio_client import Client
from tqdm import tqdm

from apiModels.meta_class import AbstractGetBibTex


class GetBibTexFromDBLP(AbstractGetBibTex):
    def __init__(self):
        self.client = Client("https://yuchenlin-rebiber.hf.space/")

    def get_bibtex(self, citation: str) -> str or bool:
        raw_bibtex = self.__pack_title2bibtex(citation)
        result = self.client.predict(
            raw_bibtex,  # str  in 'Input BIB' Textbox component
            True,  # bool  in 'Abbreviation' Checkbox component
            "url",  # List[str]  in 'Remove Keys' Checkboxgroup component
            True,  # bool  in 'Deduplicate entries.' Checkbox component
            True,  # bool  in 'Sort alphabetically by ID.' Checkbox component
            api_name="/process"
        )
        if re.search(r'author', result[0]):
            return result[0]
        return False

    def get_bibtexs(self, citations: list) -> tuple[list[str], list[str]]:
        bibtexs = []
        failed_citations = []
        for citation in tqdm(citations, desc="Getting BibTex from DBLP"):
            bibtex = self.get_bibtex(citation)
            if bibtex is not False:
                bibtexs.append(bibtex)
            else:
                failed_citations.append(citation)
        return bibtexs, failed_citations

    def __pack_title2bibtex(self, title: str) -> str:
        return "@article{" + title[0:5] + ",title={" + title + "}}"

    def isready(self):
        try:
            self.client.predict(
                "@article{test,title={test}}",  # str  in 'Input BIB' Textbox component
                True,  # bool  in 'Abbreviation' Checkbox component
                "url",  # List[str]  in 'Remove Keys' Checkboxgroup component
                True,  # bool  in 'Deduplicate entries.' Checkbox component
                True,  # bool  in 'Sort alphabetically by ID.' Checkbox component
                api_name="/process"
            )
        except Exception as e:
            raise ConnectionError("DBLP API not available")
