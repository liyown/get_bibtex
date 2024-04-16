import re

from gradio_client import Client
from tqdm import tqdm


class GetBibTexFromDBLP:
    def __init__(self):
        self.client = Client("https://yuchenlin-rebiber.hf.space/")

    def get_bibtex(self, citation):
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

    def get_bibtexs(self, citations):
        bibtexs = []
        failed_citations = []
        for citation in tqdm(citations, desc="Getting BibTex from DBLP"):
            bibtex = self.get_bibtex(citation)
            if bibtex is not False:
                bibtexs.append(bibtex)
            else:
                failed_citations.append(citation)
        return bibtexs, failed_citations

    def __pack_title2bibtex(self, title):
        return "@article{" + title[0:5] + ",title={" + title + "}}"


if __name__ == '__main__':
    str = "CBAM: Convolutional Block Attention Module"
    get_bibtex_from_dblp = GetBibTexFromDBLP()
    print(get_bibtex_from_dblp.get_bibtex(str))
