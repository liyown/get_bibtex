import re
from typing import Dict, List, Optional
from urllib.error import URLError
from urllib.request import urlopen

from serpapi import GoogleSearch
from tqdm import tqdm

from .meta_class import BibTexFetcher


class GoogleScholarBibTeX(BibTexFetcher):
    """
    Fetch BibTeX citations from Google Scholar.

    This class implements the BibTexFetcher interface for Google Scholar.
    Requires a SerpAPI key for accessing Google Scholar data.
    """

    def __init__(self, api_key: str):
        """
        Initialize Google Scholar BibTeX fetcher.

        Args:
            api_key: SerpAPI key for accessing Google Scholar
        """
        super().__init__(api_key)
        if not api_key:
            raise ValueError("SerpAPI key is required for Google Scholar access")

    def get_bibtex(self, query: str) -> Optional[str]:
        """Get BibTeX citation from Google Scholar."""
        try:
            paper = self._search_first_paper(query)
            if not paper:
                self.logger.error("No results found")
                return None

            # 优先直接获取 Google Scholar 提供的 BibTeX，确保 key 与 Scholar 一致
            scholar_bibtex = self._fetch_scholar_bibtex(paper)
            if scholar_bibtex:
                return scholar_bibtex

            self.logger.warning("Falling back to generated BibTeX for query: %s", query)
            return self._build_fallback_bibtex(paper)

        except Exception as e:
            self.logger.error(f"Error fetching from Google Scholar: {str(e)}")
            return None

    def _search_first_paper(self, query: str) -> Optional[Dict]:
        search_params = {
            "engine": "google_scholar",
            "q": query,
            "api_key": self.api_key,
            "hl": "en",
        }

        search = GoogleSearch(search_params)
        results = search.get_dict()
        papers = results.get("organic_results") or []
        if not papers:
            return None
        return papers[0]

    def _fetch_scholar_bibtex(self, paper: Dict) -> Optional[str]:
        result_id = paper.get("result_id")
        if not result_id:
            return None

        cite_search = GoogleSearch(
            {
                "engine": "google_scholar_cite",
                "q": result_id,
                "api_key": self.api_key,
            }
        )
        cite_results = cite_search.get_dict()

        bibtex_url = None
        for link_obj in cite_results.get("links", []):
            if str(link_obj.get("name", "")).lower() == "bibtex":
                bibtex_url = link_obj.get("link")
                break

        if not bibtex_url:
            return None

        try:
            with urlopen(bibtex_url, timeout=20) as response:
                data = response.read().decode("utf-8", errors="replace").strip()
        except (URLError, OSError) as e:
            self.logger.warning("Failed to download BibTeX from %s: %s", bibtex_url, e)
            return None

        return data or None

    def _build_fallback_bibtex(self, paper: Dict) -> Optional[str]:
        # 从 publication_info 中提取信息
        pub_info = paper.get("publication_info", {}).get("summary", "")
        if not pub_info:
            return None

        parts = pub_info.split(" - ")
        if not parts:
            return None

        # 提取作者
        author_part = parts[0]
        if " and " in author_part:
            authors = [a.strip() for a in author_part.split(" and ")]
        else:
            authors = [a.strip() for a in author_part.split(",") if a.strip()]

        # 提取年份
        year = None
        for part in parts[1:]:
            year_match = re.search(r"\b(19|20)\d{2}\b", part)
            if year_match:
                year = year_match.group(0)
                break

        citation_key = self._generate_citation_key(authors, year, paper.get("title", ""))

        bibtex_parts = [
            f"@{self._get_entry_type(paper)}{{{citation_key},",
            f"  title     = {{{paper.get('title', '')}}},",
            f"  author    = {{{' and '.join(authors)}}},",
        ]

        if year:
            bibtex_parts.append(f"  year      = {{{year}}},")

        if len(parts) > 1:
            venue = self._extract_venue(parts[1])
            bibtex_parts.append(f"  journal   = {{{venue}}},")

        if paper.get("link"):
            bibtex_parts.append(f"  url       = {{{paper['link']}}},")

        if "cited_by" in paper.get("inline_links", {}):
            cited_by = paper["inline_links"]["cited_by"].get("total")
            if cited_by:
                bibtex_parts.append(f"  citations = {{{cited_by}}},")

        if paper.get("doi"):
            bibtex_parts.append(f"  doi       = {{{paper['doi']}}},")

        bibtex_parts[-1] = bibtex_parts[-1].rstrip(",")
        bibtex_parts.append("}")

        return "\n".join(bibtex_parts)

    def _get_entry_type(self, paper: Dict) -> str:
        """根据论文类型确定 BibTeX 条目类型"""
        pub_info = paper.get("publication_info", {}).get("summary", "").lower()
        if any(x in pub_info for x in ["conference", "proceedings"]):
            return "inproceedings"
        elif any(x in pub_info for x in ["journal", "transactions"]):
            return "article"
        elif "arxiv" in pub_info:
            return "misc"
        elif any(x in pub_info for x in ["thesis", "dissertation"]):
            return "phdthesis"
        elif "book" in pub_info:
            return "book"
        return "misc"

    def _extract_venue(self, venue_str: str) -> str:
        """从字符串中提取期刊/会议名称"""
        venue = re.sub(r"\b(19|20)\d{2}\b", "", venue_str)
        venue = re.sub(r"-.*$", "", venue)
        return venue.strip(" ,-")

    def _generate_citation_key(self, authors: List[str], year: Optional[str], title: str) -> str:
        """Generate key as `lastname + year + first title word` when possible."""
        first_author_lastname = authors[0].split()[0] if authors else "unknown"
        normalized_title = re.sub(r"[^a-zA-Z0-9\s]", " ", title.lower())
        title_words = [word for word in normalized_title.split() if word]
        first_title_word = title_words[0] if title_words else ""
        return f"{first_author_lastname.lower()}{year or ''}{first_title_word}"

    def get_multiple_bibtex(self, queries: List[str]) -> Dict[str, Optional[str]]:
        """
        Fetch multiple BibTeX citations from Google Scholar.

        Args:
            queries: List of search queries

        Returns:
            Dict[str, Optional[str]]: Dictionary mapping queries to their BibTeX citations
        """
        results = {}

        for query in tqdm(queries, desc="Fetching from Google Scholar"):
            bibtex = self.get_bibtex(query)
            results[query] = bibtex

            # Add delay to comply with rate limits
            import time

            time.sleep(2)  # Google Scholar is more strict about rate limiting

        return results

    def search_papers(self, query: str, limit: int = 5) -> List[Dict]:
        """Search for papers in Google Scholar."""
        try:
            search_params = {
                "engine": "google_scholar",
                "q": query,
                "api_key": self.api_key,
                "num": str(limit),
            }

            search = GoogleSearch(search_params)
            results = search.get_dict()

            if "organic_results" not in results:
                return []

            papers = []
            for result in results["organic_results"][:limit]:
                paper = {
                    "title": result.get("title"),
                    "authors": result.get("publication_info", {}).get("authors", []),
                    "year": result.get("publication_info", {}).get("year"),
                    "citation_id": result.get("inline_links", {})
                    .get("cited_by", {})
                    .get("cites", ""),
                }
                papers.append(paper)

            return papers

        except Exception as e:
            self.logger.error(f"Error searching Google Scholar: {str(e)}")
            return []
