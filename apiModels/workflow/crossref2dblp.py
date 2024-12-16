from typing import List, Dict, Optional, Tuple
from ..get_bibtex_from_crossref import CrossRefBibTeX
from ..get_bibtex_from_dblp import DBLPBibTeX
import logging

logger = logging.getLogger(__name__)

class CrossRefToDBLP:
    """
    Workflow to fetch BibTeX from CrossRef and fallback to DBLP if needed.
    
    This class implements a workflow that first tries to get citations from CrossRef,
    and if that fails, falls back to DBLP as a backup source.
    """

    def __init__(self, email: Optional[str] = None):
        """
        Initialize the workflow.

        Args:
            email: Optional email for CrossRef's polite pool
        """
        self.crossref = CrossRefBibTeX(email)
        self.dblp = DBLPBibTeX()
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_bibtex(self, query: str) -> Optional[str]:
        """
        Get BibTeX citation using CrossRef with DBLP as fallback.

        Args:
            query: DOI or search query

        Returns:
            Optional[str]: BibTeX citation if found, None otherwise
        """
        try:
            # Try CrossRef first
            bibtex = self.crossref.get_bibtex(query)
            if bibtex:
                self.logger.info(f"Found citation in CrossRef for: {query}")
                return bibtex

            # Fallback to DBLP
            self.logger.info(f"Trying DBLP as fallback for: {query}")
            bibtex = self.dblp.get_bibtex(query)
            if bibtex:
                self.logger.info(f"Found citation in DBLP for: {query}")
                return bibtex

            self.logger.warning(f"No citation found for: {query}")
            return None

        except Exception as e:
            self.logger.error(f"Error in workflow: {str(e)}")
            return None

    def get_multiple_bibtex(self, queries: List[str]) -> Tuple[Dict[str, str], List[str]]:
        """
        Get multiple BibTeX citations using CrossRef with DBLP as fallback.

        Args:
            queries: List of DOIs or search queries

        Returns:
            Tuple[Dict[str, str], List[str]]: 
                - Dictionary of successful queries and their BibTeX citations
                - List of failed queries
        """
        successful = {}
        failed = []

        for query in queries:
            bibtex = self.get_bibtex(query)
            if bibtex:
                successful[query] = bibtex
            else:
                failed.append(query)

        return successful, failed

    def search_publication(self, query: str) -> Dict[str, List[Dict]]:
        """
        Search for publications in both CrossRef and DBLP.

        Args:
            query: Search query

        Returns:
            Dict[str, List[Dict]]: Dictionary containing results from both sources
        """
        results = {
            'crossref': [],
            'dblp': []
        }

        try:
            # Search in CrossRef
            crossref_results = self.crossref.search_works(query)
            if crossref_results:
                results['crossref'] = crossref_results

            # Search in DBLP
            dblp_results = self.dblp.search_publications(query)
            if dblp_results:
                results['dblp'] = dblp_results

        except Exception as e:
            self.logger.error(f"Error searching publications: {str(e)}")

        return results

    def save_results(self, results: Dict[str, str], output_path: str) -> bool:
        """
        Save successful BibTeX citations to file.

        Args:
            results: Dictionary of queries and their BibTeX citations
            output_path: Path to save the citations

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for query, bibtex in results.items():
                    f.write(f"% Query: {query}\n")
                    f.write(f"{bibtex}\n\n")
            return True
        except Exception as e:
            self.logger.error(f"Error saving results: {str(e)}")
            return False
