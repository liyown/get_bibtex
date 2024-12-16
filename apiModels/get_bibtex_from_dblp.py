import requests
from typing import Dict, List, Optional
from tqdm import tqdm
from .meta_class import BibTexFetcher

class DBLPBibTeX(BibTexFetcher):
    """
    Fetch BibTeX citations from DBLP.
    
    This class implements the BibTexFetcher interface for DBLP (dblp.org).
    DBLP is a comprehensive computer science bibliography database.
    """

    def __init__(self):
        """Initialize DBLP fetcher."""
        super().__init__()
        self.base_url = "https://dblp.org/search/publ/api"  # 论文搜索 API
        self.bibtex_url = "https://dblp.org/rec/{}.bib"  # BibTeX 获取 API
        self.headers = {
            'Accept': 'application/json'  # 指定返回 JSON 格式
        }

    def get_bibtex(self, query: str) -> Optional[str]:
        """
        Get BibTeX citation from DBLP.

        Args:
            query: Search query (title or DBLP key)

        Returns:
            Optional[str]: BibTeX citation if found, None otherwise
        """
        try:
            # 如果是 DBLP key，直接获取 BibTeX
            if '/' in query:  # DBLP key 格式如 'conf/naacl/DevlinCLT19'
                url = self.bibtex_url.format(query)
                response = requests.get(url)
                if response.status_code == 200:
                    return response.text.strip()
                self.logger.error(f"Failed to fetch BibTeX. Status code: {response.status_code}")
                return None

            # 否则通过搜索 API 查找
            params = {
                'q': query,
                'format': 'json',
                'h': 1,  # 限制返回结果数量
                'c': 0   # 不需要自动补全
            }

            response = requests.get(
                self.base_url,
                params=params,
                headers=self.headers
            )

            if response.status_code != 200:
                self.logger.error(f"Failed to fetch BibTeX. Status code: {response.status_code}")
                return None

            data = response.json()
            hits = data.get('result', {}).get('hits', {}).get('hit', [])
            
            if not hits:
                return None

            # Get the first result's key
            paper_info = hits[0].get('info', {})
            key = paper_info.get('key')
            
            if not key:
                return None

            # 获取 BibTeX
            url = self.bibtex_url.format(key)
            response = requests.get(
                url,
                headers={'Accept': 'text/plain'}  # BibTeX 应该以纯文本格式返回
            )

            if response.status_code == 200:
                return response.text.strip()

            self.logger.error(f"Failed to fetch BibTeX. Status code: {response.status_code}")
            return None

        except Exception as e:
            self.logger.error(f"Error fetching from DBLP: {str(e)}")
            return None

    def get_multiple_bibtex(self, queries: List[str]) -> Dict[str, Optional[str]]:
        """
        Fetch multiple BibTeX citations from DBLP.

        Args:
            queries: List of search queries

        Returns:
            Dict[str, Optional[str]]: Dictionary mapping queries to their BibTeX citations
        """
        results = {}
        
        for query in tqdm(queries, desc="Fetching from DBLP"):
            bibtex = self.get_bibtex(query)
            results[query] = bibtex
            
            # Add small delay to be nice to the API
            if len(queries) > 10:
                import time
                time.sleep(1)
        
        return results

    def search_publications(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Search for publications in DBLP.

        Args:
            query: Search query
            limit: Maximum number of results to return

        Returns:
            List[Dict]: List of publication metadata
        """
        try:
            params = {
                'q': query,
                'format': 'json',
                'h': min(limit, 1000),  # API 限制最大返回 1000 条
                'c': 0  # 不需要自动补全
            }

            response = requests.get(
                self.base_url,
                params=params,
                headers=self.headers
            )

            if response.status_code != 200:
                self.logger.error(f"Failed to search DBLP. Status code: {response.status_code}")
                return []

            data = response.json()
            hits = data.get('result', {}).get('hits', {}).get('hit', [])
            
            papers = []
            for hit in hits[:limit]:
                info = hit.get('info', {})
                paper = {
                    'title': info.get('title'),
                    'authors': self._extract_authors(info.get('authors', {})),
                    'year': info.get('year'),
                    'venue': info.get('venue'),
                    'type': info.get('type'),
                    'key': info.get('key'),
                    'doi': info.get('doi'),
                    'url': info.get('url')
                }
                papers.append(paper)
                
            return papers

        except Exception as e:
            self.logger.error(f"Error searching DBLP: {str(e)}")
            return []

    def _extract_authors(self, authors_data: Dict) -> List[str]:
        """Extract author names from DBLP author data structure."""
        if not authors_data:
            return []
        
        authors = authors_data.get('author', [])
        if isinstance(authors, dict):
            authors = [authors]
        
        return [
            author['text'] if isinstance(author, dict) else author
            for author in authors
        ]
