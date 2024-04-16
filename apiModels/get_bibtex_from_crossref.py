import requests
from requests.adapters import HTTPAdapter
from tqdm import tqdm

from apiModels.meta_class import AbstractGetBibTex


class GetBibTex(AbstractGetBibTex):
    """
    Get BibTex from citation strings using the Google Scholar API
    Done by: liuyaowen
    Since: 2024-4-10
    """
    def __init__(self, email, max_retries=5, rows=4):
        """
        :param email: The email address to be used in the User-Agent
        :param max_retries: The maximum number of retries to be used in the HTTPAdapter
        :param rows: The number of rows to be requested from the Crossref API
        """
        self.session = requests.Session()
        # 设置重试机制 5次
        self.session.mount("http://", HTTPAdapter(max_retries=max_retries))  # set max retries
        self.session.mount("https://", HTTPAdapter(max_retries=max_retries))
        self.api_url = "https://api.crossref.org/works"
        self.bibtex_api_url = "https://api.crossref.org/works/{doi}/transform/application/x-bibtex"
        self.headers = {"User-Agent": "MyApp/1.0 ({})".format(email)}
        self.params = {"query.bibliographic": "", "rows": rows}

    def __get_doi(self, citation):
        """
        :param citation:  a citation string
        :return:  a list of paper objects
        """
        self.params["query.bibliographic"] = citation
        response = self.session.get(self.api_url, headers=self.headers, params=self.params)
        data = response.json()
        Items = data["message"]["items"]
        for item in Items:
            # to avoid the case where the title is too short and matches the sub words in the citation
            if item["title"][0].replace(" ", "").lower() in citation.replace(" ", "").lower() and len(
                    item["title"][0]) > 10:
                return item["DOI"]
        return None

    def get_bibtex(self, citation: str) -> str or bool:
        """
        :param citation:  a citation string
        :return:  BibTex string, or False if not found
        """
        doi = self.__get_doi(citation)
        if doi:
            bibtex_url = self.bibtex_api_url.format(doi=doi)
            bibtex_response = self.session.get(bibtex_url)
            return bibtex_response.text
        else:
            return False

    def get_bibtexs(self, citations: list) -> tuple[list[str], list[str]]:
        """
        :param citations:  a list of citation strings
        :return:  a list of BibTex strings
        """
        assert isinstance(citations, list)
        bibtexs = []
        failed_citations = []
        for citation in tqdm(citations, desc="Getting BibTex from CrossRef"):
            bibtex = self.get_bibtex(citation)
            if bibtex is not False:
                bibtexs.append(bibtex)
            else:
                failed_citations.append(citation)
        return bibtexs, failed_citations

    def isready(self):
        """
        :return:  True if the API is available
        """
        try:
            self.session.get(self.api_url, headers=self.headers, params=self.params)
        except Exception as e:
            raise ConnectionError("Crossref API not available")
