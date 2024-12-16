import requests
from typing import Dict, List, Optional
from tqdm import tqdm
from .meta_class import BibTexFetcher

class CrossRefBibTeX(BibTexFetcher):
    """
    Fetch BibTeX citations from CrossRef.
    """

    def __init__(self, email: str):
        """
        Initialize CrossRef fetcher.

        Args:
            email: Email address for polite pool
        """
        super().__init__()
        self.base_url = "https://api.crossref.org"
        self.headers = {
            'User-Agent': f'GetBibTeX/1.0 (mailto:{email})'
        }

    def get_multiple_bibtex(self, queries: List[str]) -> Dict[str, Optional[str]]:
        """
        Fetch multiple BibTeX citations from CrossRef.

        Args:
            queries: List of DOIs or search queries

        Returns:
            Dict[str, Optional[str]]: Dictionary mapping queries to their BibTeX citations
        """
        results = {}
        
        for query in tqdm(queries, desc="Fetching from CrossRef"):
            bibtex = self.get_bibtex(query)
            results[query] = bibtex
            
            # Add small delay to be nice to the API
            if len(queries) > 10:
                import time
                time.sleep(1)
        
        return results

    def get_bibtex(self, query: str) -> Optional[str]:
        """
        Get BibTeX citation from CrossRef.

        Args:
            query: Search query (DOI or title)

        Returns:
            Optional[str]: BibTeX citation if found, None otherwise
        """
        try:
            # 如果是 DOI，直接获取
            if self._is_doi(query):
                bibtex = self._get_bibtex_by_doi(query)
                # 验证 BibTeX 是否包含必要字段
                if bibtex and self._validate_bibtex(bibtex):
                    return bibtex
                return None

            # 否则通过搜索 API 查找
            results = self.search_works(query, limit=1)
            if not results:
                return None

            doi = results[0].get('DOI')
            if not doi:
                return None

            bibtex = self._get_bibtex_by_doi(doi)
            # 验证 BibTeX 是否包含必要字段
            if bibtex and self._validate_bibtex(bibtex):
                return bibtex
            return None

        except Exception as e:
            self.logger.error(f"Error fetching from CrossRef: {str(e)}")
            return None

    def search_works(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Search for works in CrossRef.

        Args:
            query: Search query
            limit: Maximum number of results to return

        Returns:
            List[Dict]: List of work metadata
        """
        try:
            # 构建查询参数
            params = {
                'query.bibliographic': query,  # 使用书目字段搜索
                'rows': str(limit),
                'select': 'DOI,title,author,published,type,container-title',  # 只获取需要的字段
                'sort': 'relevance',  # 按相关性排序
                'order': 'desc'
            }

            response = requests.get(
                f"{self.base_url}/works",
                params=params,
                headers=self.headers
            )

            if response.status_code != 200:
                self.logger.error(f"Failed to search CrossRef. Status code: {response.status_code}")
                return []

            data = response.json()
            items = data.get('message', {}).get('items', [])

            works = []
            for item in items:
                work = {
                    'DOI': item.get('DOI'),
                    'title': self._get_first(item.get('title', [])),
                    'authors': self._extract_authors(item.get('author', [])),
                    'year': self._extract_year(item.get('published')),
                    'type': item.get('type'),
                    'container-title': self._get_first(item.get('container-title', []))
                }
                works.append(work)

            return works

        except Exception as e:
            self.logger.error(f"Error searching CrossRef: {str(e)}")
            return []

    def _get_bibtex_by_doi(self, doi: str) -> Optional[str]:
        """Get BibTeX citation for a DOI."""
        try:
            response = requests.get(
                f"{self.base_url}/works/{doi}/transform/application/x-bibtex",
                headers=self.headers
            )

            if response.status_code == 200 and response.text.strip():
                return response.text.strip()

            self.logger.error(f"Failed to get BibTeX. Status code: {response.status_code}")
            return None

        except Exception as e:
            self.logger.error(f"Error getting BibTeX: {str(e)}")
            return None

    def _extract_year(self, date_info: Dict) -> Optional[str]:
        """Extract year from CrossRef date information."""
        if not date_info:
            return None
        
        parts = date_info.get('date-parts', [[]])[0]
        return str(parts[0]) if parts else None

    def _extract_authors(self, authors: List[Dict]) -> List[str]:
        """Extract author names from CrossRef author information."""
        return [
            f"{author.get('family', '')}, {author.get('given', '')}"
            for author in authors
            if author.get('family') or author.get('given')
        ]

    def _get_first(self, items: List) -> Optional[str]:
        """Get first item from a list or None."""
        return items[0] if items else None

    def _is_doi(self, query: str) -> bool:
        """Check if a query is a DOI."""
        try:
            query = query.strip().lower()
            # 更严格的 DOI 验证
            parts = query.split('/')
            return (
                len(parts) == 2 
                and parts[0].startswith('10.') 
                and all(p.strip() for p in parts)
            )
        except:
            return False

    def _validate_bibtex(self, bibtex: str) -> bool:
        """
        验证 BibTeX 是否包含所有必要字段
        
        Args:
            bibtex: BibTeX 字符串
            
        Returns:
            bool: True 如果包含所有必要字段，否则 False
        """
        bibtex = bibtex.lower()
        required_fields = ['title', 'author', 'year']
        return all(field in bibtex for field in required_fields)
