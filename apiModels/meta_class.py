from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BibTexFetcher(ABC):
    """
    Abstract base class for fetching BibTeX citations from various sources.
    
    This class defines the interface that all BibTeX fetchers must implement.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the BibTeX fetcher.

        Args:
            api_key: Optional API key for services that require authentication
        """
        self.api_key = api_key
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def get_bibtex(self, query: str) -> Optional[str]:
        """
        Fetch BibTeX citation for a given query.

        Args:
            query: Search query (DOI, title, or other identifier)

        Returns:
            Optional[str]: BibTeX citation if found, None otherwise
        """
        pass

    @abstractmethod
    def get_multiple_bibtex(self, queries: List[str]) -> Dict[str, Optional[str]]:
        """
        Fetch multiple BibTeX citations for a list of queries.

        Args:
            queries: List of search queries

        Returns:
            Dict[str, Optional[str]]: Dictionary mapping queries to their BibTeX citations
        """
        pass

    def save_bibtex(self, bibtex: str, output_path: str) -> bool:
        """
        Save BibTeX citation to a file.

        Args:
            bibtex: BibTeX citation string
            output_path: Path to save the file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            mode = 'a' if output_file.exists() else 'w'
            with open(output_file, mode, encoding='utf-8') as f:
                f.write(bibtex + '\n\n')
            return True
        except Exception as e:
            self.logger.error(f"Error saving BibTeX: {str(e)}")
            return False

    def _validate_response(self, response: Any) -> bool:
        """
        Validate API response.

        Args:
            response: API response object

        Returns:
            bool: True if valid, False otherwise
        """
        if response is None:
            return False
        return True

    def _clean_bibtex(self, bibtex: str) -> str:
        """
        Clean and format BibTeX string.

        Args:
            bibtex: Raw BibTeX string

        Returns:
            str: Cleaned BibTeX string
        """
        if not bibtex:
            return ""
        
        # Remove extra whitespace and normalize line endings
        bibtex = bibtex.strip()
        bibtex = '\n'.join(line.strip() for line in bibtex.splitlines())
        
        # Ensure the BibTeX ends with a closing brace
        if not bibtex.endswith('}'):
            bibtex += '\n}'
            
        return bibtex
