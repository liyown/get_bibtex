import requests
from serpapi import GoogleSearch
from tqdm import tqdm
from typing import Tuple, List, Any, Union


class GetBibTexFromGoogleScholar:
    """
    Get BibTex from citation strings using the Google Scholar API
    Done by: liuyaowen
    Since: 2024-4-10
    """
    # citation style
    MPA = 0
    APA = 1
    CHICAGO = 2
    HARVARD = 3
    VANCOUVER = 4

    def __init__(self, api_key=None, flag=False, style=1):
        """
        :param api_key:  google scholar api key
        :param flag:  whether to use link to get bibtex
        :param style:  the style of citation
        """
        self.api_key = api_key
        self.flag = flag  # whether to use link to get bibtex
        self.style = style

    def get_bibtex(self, citation: str) -> str or bool:
        """
        :param citation: a citation string
        :return:    if flag is True, return bibtex else return snippet
                    and if link request failed, return snippet
        """
        # if the citation is not found, return False
        if self.__get_result_id(citation) is False:
            return False
        params = {
            "engine": "google_scholar_cite",
            "q": self.__get_result_id(citation),
            "api_key": self.api_key
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        link = results["links"][0]["link"]
        cite = results["citations"][self.style]["snippet"]
        if self.flag is True:
            tqdm.write("attempting to get bibtex by link")
            try:
                resp = requests.get(link)
                if resp.status_code == 200:
                    return resp.text
            except Exception as e:
                print(e)
                self.flag = False
                tqdm.write("get bibtex failed by link, return snippet")
        return cite

    def get_bibtexs(self, citations: List[str]) -> Tuple[List[str], List[str]]:
        """
        :param citations: a list of citation strings
        :return:    if flag is True, return bibtexs else return snippets
                    and if link request failed, return snippets
        """
        bibtexs = []
        snippets = []
        for citation in tqdm(citations):
            bibtex = self.get_bibtex(citation)
            if bibtex:
                bibtexs.append(bibtex)
            else:
                snippets.append(citation)
        return bibtexs, snippets

    def __get_result_id(self, query):
        """
        :param query: a citation string
        :return:    result_id from google scholar
        """
        params = {
            "engine": "google_scholar",
            "q": query,
            "api_key": self.api_key
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results["organic_results"]
        for result in organic_results:
            result_ = result["title"].replace(" ", "").lower()
            if result_[-1] == ".":
                result_ = result_[:-1]
                print(result_)
            query_ = query.replace(" ", "").lower()
            # verify the result is the paper we want to find,beacuse the result may not be the word in the citation,
            # so we need sure the paper's length is more than 10 so that decrease the probability of wrong result
            if result_ in query_ and len(result_) > 10:
                return result["result_id"]
            return False