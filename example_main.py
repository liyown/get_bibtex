from apiModels.get_bibtex_from_crossref import GetBibTex
from apiModels.get_bibtex_from_google_scholar import GetBibTexFromGoogleScholar

if __name__ == '__main__':
    google_scholar_api_key = "your_google_scholar_api_key"
    get_bibtex_from_crossref = GetBibTex("your_email_address")
    # use APA
    get_bibtex_from_google_scholar = GetBibTexFromGoogleScholar(google_scholar_api_key, GetBibTexFromGoogleScholar.APA)
    # open the file that contains the raw bibliography
    # each line is one raw bibliography
    with open("test/inputfile/Bibliographyraw.txt", "r", encoding='utf-8') as f:
        raws = f.readlines()
    # get bibtex from CrossRef
    success_bibtexs_crossref, failed_results = get_bibtex_from_crossref.get_bibtexs(raws)
    # get bibtex from Google Scholar
    success_bibtexs_google, failed_results = get_bibtex_from_google_scholar.get_bibtexs(failed_results)
    # write the bibtex to the output file
    with open("test/outputfile/BibliographyCrossRef.txt", "w", encoding='utf-8') as f:
        for bibtex in success_bibtexs_crossref:
            f.write(bibtex)
    # write the bibtex to the output file
    with open("test/outputfile/BibliographyGoogleScholar.txt", "w", encoding='utf-8') as f:
        for index, bibtex in enumerate(success_bibtexs_google):
            f.write("[]".format(index) + " " + bibtex + "\n")
    # write the failed results to the output file
    with open("test/outputfile/not_find.txt", "w", encoding='utf-8') as f:
        for result in failed_results:
            f.write(result+"\n")
    # print the number of successful results and failed results
    print("find bibtex from CrossRef: ", len(success_bibtexs_crossref))
    print("find bibtex from Google Scholar: ", len(success_bibtexs_google))
    print("not find: ", len(failed_results))

