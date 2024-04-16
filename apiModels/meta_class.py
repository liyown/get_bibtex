class AbstractGetBibTex:
    """
    Abstract class for getting
    BibTex from citation strings
    """

    def get_bibtex(self, citation: str) -> str or bool:
        raise NotImplementedError

    def get_bibtexs(self, citations: list) -> tuple[list[str], list[str]]:
        raise NotImplementedError

    def isready(self):
        raise NotImplementedError
