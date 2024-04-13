
# get bibtex from crossref and google scholar

## Introduction
This is a simple python script to get bibtex from crossref and google scholar. It is useful when you want to get bibtex for a list of DOIs or titles.

## Depend
- requests // for http request
- re // for regular expression
- serpapi // for google scholar
- tqdm // for progress bar

## Usage

look at the example in `example_main.py`

```python
from apiModel.getbibtex_from_crossref import GetBibTex

get_bibtex_from_crossref = GetBibTex("your email")
doi = "10.1145/3313831.3376234"
bibtex = get_bibtex_from_crossref.get_bibtex(doi)

# or use title
title = "A Survey of Modern Authorship Attribution Methods"
bibtex = get_bibtex_from_crossref.get_bibtex(title)
```

