from typing import Dict, List, Optional
from tqdm import tqdm
from serpapi import GoogleSearch
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
        """
        Get BibTeX citation from Google Scholar.
        """
        try:
            # 直接搜索论文
            search_params = {
                "engine": "google_scholar",
                "q": query,
                "api_key": self.api_key,
                "hl": "en"  # 使用英文界面
            }
            
            search = GoogleSearch(search_params)
            results = search.get_dict()
            if "organic_results" not in results or not results["organic_results"]:
                self.logger.error("No results found")
                return None
                
            # Get the first result
            paper = results["organic_results"][0]
            
            # 从 publication_info 中提取信息
            pub_info = paper.get('publication_info', {}).get('summary', '')
            if not pub_info:
                return None
                
            # 解析 publication_info
            # 格式可能是以下几种:
            # 1. "Author1, Author2... - Journal/Conference, Year - Source"
            # 2. "Author1 - Journal/Conference, Year"
            # 3. "Author1, Author2... - Year"
            parts = pub_info.split(' - ')
            if not parts:
                return None
                
            # 提取作者
            author_part = parts[0]
            authors = []
            if ' and ' in author_part:
                authors = [a.strip() for a in author_part.split(' and ')]
            else:
                authors = [a.strip() for a in author_part.split(',') if a.strip()]
            
            # 提取年份
            year = None
            for part in parts[1:]:
                # 查找年份格式 (YYYY)
                import re
                year_match = re.search(r'\b(19|20)\d{2}\b', part)
                if year_match:
                    year = year_match.group(0)
                    break
            
            # 生成引用 key
            first_author = authors[0].split()[-1] if authors else 'Unknown'
            citation_key = f"{first_author.lower()}{year or ''}"
            
            # 构建 BibTeX
            bibtex_parts = [
                f"@{self._get_entry_type(paper)}{{{citation_key},",
                f"  title     = {{{paper.get('title', '')}}},",
                f"  author    = {{{' and '.join(authors)}}},"
            ]
            
            if year:
                bibtex_parts.append(f"  year      = {{{year}}},")
                
            if len(parts) > 1:
                venue = self._extract_venue(parts[1])
                bibtex_parts.append(f"  journal   = {{{venue}}},")
                
            if paper.get('link'):
                bibtex_parts.append(f"  url       = {{{paper['link']}}},")
                
            # 添加其他可用字段
            if 'cited_by' in paper.get('inline_links', {}):
                cited_by = paper['inline_links']['cited_by'].get('total')
                if cited_by:
                    bibtex_parts.append(f"  citations = {{{cited_by}}},")
            
            # 添加 DOI 如果存在
            if paper.get('doi'):
                bibtex_parts.append(f"  doi       = {{{paper['doi']}}},")
            
            # 移除最后一个逗号并添加结束括号
            bibtex_parts[-1] = bibtex_parts[-1].rstrip(',')
            bibtex_parts.append("}")
            
            bibtex = '\n'.join(bibtex_parts)
            return bibtex
            
        except Exception as e:
            self.logger.error(f"Error fetching from Google Scholar: {str(e)}")
            print(f"Debug - Exception details: {str(e)}")
            return None

    def _get_entry_type(self, paper: Dict) -> str:
        """
        根据论文类型确定 BibTeX 条目类型
        """
        pub_info = paper.get('publication_info', {}).get('summary', '').lower()
        if any(x in pub_info for x in ['conference', 'proceedings']):
            return 'inproceedings'
        elif any(x in pub_info for x in ['journal', 'transactions']):
            return 'article'
        elif 'arxiv' in pub_info:
            return 'misc'
        elif any(x in pub_info for x in ['thesis', 'dissertation']):
            return 'phdthesis'
        elif 'book' in pub_info:
            return 'book'
        return 'misc'
        
    def _extract_venue(self, venue_str: str) -> str:
        """
        从字符串中提取期刊/会议名称
        """
        # 移除年份
        import re
        venue = re.sub(r'\b(19|20)\d{2}\b', '', venue_str)
        # 移除出版商信息
        venue = re.sub(r'-.*$', '', venue)
        # 清理并返回
        return venue.strip(' ,-')

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
        """
        Search for papers in Google Scholar.
        """
        try:
            search_params = {
                "engine": "google_scholar",
                "q": query,
                "api_key": self.api_key,
                "num": str(limit)  # SerpAPI 需要字符串类型的参数
            }
            
            search = GoogleSearch(search_params)
            results = search.get_dict()
            
            if "organic_results" not in results:
                return []
                
            papers = []
            for result in results['organic_results'][:limit]:
                paper = {
                    'title': result.get('title'),
                    'authors': result.get('publication_info', {}).get('authors', []),
                    'year': result.get('publication_info', {}).get('year'),
                    'citation_id': result.get('inline_links', {}).get('cited_by', {}).get('cites', '')
                }
                papers.append(paper)
                
            return papers

        except Exception as e:
            self.logger.error(f"Error searching Google Scholar: {str(e)}")
            return []
