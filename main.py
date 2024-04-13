from apiModels.get_bibtex_from_crossref import GetBibTex
from apiModels.get_bibtex_from_google_scholar import GetBibTexFromGoogleScholar

if __name__ == '__main__':
    google_scholar_api_key = "cbb23f2e312f9f3e3ea272c4903781db4540cb36afee4063b4ad8df3421edee7"
    get_bibtex_from_crossref = GetBibTex("1536727925@qq.com")
    get_bibtex_from_google_scholar = GetBibTexFromGoogleScholar(google_scholar_api_key, GetBibTexFromGoogleScholar.APA)

    with open("inputfile/Bibliographyraw.txt", "r", encoding='utf-8') as f:
        raws = f.readlines()

    success_bibtexs_crossref, failed_results = get_bibtex_from_crossref.get_bibtexs(raws)

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

