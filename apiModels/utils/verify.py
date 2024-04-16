import re

from tqdm import tqdm


def verify_bibtex(bibtexs: list, raws: str):
    """
    verify bibtexs whether all in raws
    :param bibtexs: List of output bibtex
    :param raws: str for all citation, you can use f.read to get it
    :return: the citation not in raws, means the bibtex is wrong
        but it is less likely to happen, "get_bibtex_...“ has been verified
    """
    res = []
    for bibtex in tqdm(bibtexs):
        if bibtex.strip() == "":
            continue
        result = re.search(r"title={.*?}", bibtex).group(0)
        # 取出title={title}中的title 正则做法
        title = result[7:-1]
        # 查询title是否在raws中 正则做法
        try:
            aa = re.search(title.lower(), raws.lower()).group()
        except AttributeError:
            res.append(title)
    return res
