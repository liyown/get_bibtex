需求：在使用latex写论文的时候，你是否有这个需求，需要将引用转换为bibtex格式，如果文献量很大，这个重复工作实在不值得做，如果你实现使用了文献管理工具，例如endnote、zotero，可以一件导出，但是没有的话，本文提供一个解决方案

方案：crossref API+google scholar API

crossref 是最大的外文doi发布平台，基本包含了所有的外文文献的元数据，但是也有一些包括不限于arXiv等文献是查询不到了，这个时候需要google scholar帮忙

为了节省大家的时间，这两个api我已经进行了封装，只需要使用pip下载下来

```
pip install get_bibtex
```

之后可以按照下面的使用方法

```
from apiModels.get_bibtex_from_crossref import GetBibTex
from apiModels.get_bibtex_from_google_scholar import GetBibTexFromGoogleScholar

if __name__ == '__main__':
    google_scholar_api_key = "your_google_scholar_api_key"
    get_bibtex_from_crossref = GetBibTex("1536727925@qq.com")
    get_bibtex_from_google_scholar = GetBibTexFromGoogleScholar(google_scholar_api_key, GetBibTexFromGoogleScholar.APA)

    with open("inputfile/Bibliographyraw.txt", "r", encoding='utf-8') as f:
        raws = f.readlines()
    
    # get bibtex from CrossRef and failed search results
    success_bibtexs_crossref, failed_results = get_bibtex_from_crossref.get_bibtexs(raws)
    
    # for each failed search result, get bibtex from Google Scholar
    success_bibtexs_google, failed_results = get_bibtex_from_google_scholar.get_bibtexs(failed_results)

    with open("outputfile/BibliographyCrossRef.txt", "w", encoding='utf-8') as f:
        for bibtex in success_bibtexs_crossref:
            f.write(bibtex)

    with open("outputfile/BibliographyGoogleScholar.txt", "w", encoding='utf-8') as f:
        for index, bibtex in enumerate(success_bibtexs_google):
            f.write("[]".format(index) + " " + bibtex + "\n")

    with open("outputfile/not_find.txt", "w", encoding='utf-8') as f:
        for result in failed_results:
            f.write(result+"\n")

    print("find bibtex from CrossRef: ", len(success_bibtexs_crossref))
    print("find bibtex from Google Scholar: ", len(success_bibtexs_google))
    print("not find: ", len(failed_results))
```

关键代码解释

```python
Bibliographyraw.txt里面是需要查询的文件
例如：
J. Hu, L. Shen, S. Albanie, G. Sun, and A. Vedaldi, “Gather-Excite: Exploiting Feature Context in Convolutional Neural Networks.” arXiv, Jan. 12, 2019. doi: 10.48550/arXiv.1810.12348.
X. Wang, R. Girshick, A. Gupta, and K. He, “Non-local Neural Networks.” arXiv, Apr. 13, 2018. doi: 10.48550/arXiv.1711.07971.
------------------
```

```python
success_bibtexs_crossref, failed_results = get_bibtex_from_crossref.get_bibtexs(raws)
返回的第一个参数为bibtex列表，第二个为没有查询到的原文献
```



-------------------

```python
success_bibtexs_google, failed_results = get_bibtex_from_google_scholar.get_bibtexs(failed_results)
将没有查到的文献继续使用google API查询，一般都是可以查询到了，没有文献在google scholar查询不到了吧
```

```python
提示，这里返回的其实是APA格式的，在上面初始化指定，也有一个参数可以设置返回bibtex格式，例如
get_bibtex_from_google_scholar = GetBibTexFromGoogleScholar(google_scholar_api_key, GetBibTexFromGoogleScholar.APA, flag = True)
但是需要设置代理服务器，例如：
import os
import re
import requests
os.environ["http_proxy"]="127.0.0.1:7890"
os.environ["https_proxy"]="127.0.0.1:7890"
```

！！！！！！！注意：需要先去申请API，每个月有100的免费查询次数，一般是够用的，在serpapi.com申请

之后的代码都一目了然了哈哈

当然也有请求单个查询的：

```python
get_bibtex() 去掉s就可以了 
```

欢迎改进

