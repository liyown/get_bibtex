import re

from tqdm import tqdm


def verify_bibtex(bibtexs, raws):
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
            print(title)
