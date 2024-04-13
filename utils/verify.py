import re

from tqdm import tqdm

with open("../outputfile/Bibliography.txt", "r", encoding='utf-8') as f:
    bibtexs = f.readlines()

with open("../inputfile/Bibliographyraw.txt", "r", encoding='utf-8') as f:
    raws = f.read()

for bibtex in tqdm(bibtexs):
    if bibtex.strip() == "":
        continue
    result = re.search(r'title={.*?}', bibtex).group(0)
    # 取出title={title}中的title 正则做法
    title = result[7:-1]
    # 查询title是否在raws中 正则做法
    try:
        aa = re.search(title.lower(), raws.lower()).group()
    except AttributeError:
        print(title)





