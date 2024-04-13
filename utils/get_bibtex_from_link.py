import os
import re
import requests
os.environ["http_proxy"]="127.0.0.1:7890"
os.environ["https_proxy"]="127.0.0.1:7890"

with open("../outputfile/Error.txt", "r", encoding="utf-8") as f:
    papers = f.readlines()

for paper in papers:
    link = re.search(r'https:.*', paper).group(0)
    resp = requests.get(link)
    print(resp.text)