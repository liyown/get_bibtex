from typing import List, Dict, Optional, Type
from ..meta_class import BibTexFetcher
from tqdm import tqdm
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class WorkflowBuilder:
    """
    A flexible workflow builder for chaining multiple BibTeX fetchers.
    
    This class allows creating custom workflows by combining multiple BibTeX
    fetchers in a specified order, with configurable fallback behavior.
    """

    def __init__(self):
        """Initialize the workflow builder."""
        self.fetchers: List[BibTexFetcher] = []
        self.logger = logging.getLogger(self.__class__.__name__)

    def add_fetcher(self, fetcher: BibTexFetcher) -> 'WorkflowBuilder':
        """
        Add a BibTeX fetcher to the workflow.

        Args:
            fetcher: Instance of a BibTexFetcher

        Returns:
            WorkflowBuilder: self for method chaining
        """
        if not isinstance(fetcher, BibTexFetcher):
            raise ValueError(
                f"Fetcher must be an instance of BibTexFetcher, got {type(fetcher)}"
            )
        self.fetchers.append(fetcher)
        return self

    def get_bibtex(self, query: str) -> Optional[str]:
        """
        Try to get BibTeX citation using all configured fetchers in order.

        Args:
            query: Search query (DOI, title, etc.)

        Returns:
            Optional[str]: First successful BibTeX citation found, or None if all fail
        """
        for fetcher in self.fetchers:
            try:
                bibtex = fetcher.get_bibtex(query)
                if bibtex:
                    self.logger.info(
                        f"Found citation using {fetcher.__class__.__name__} for: {query}"
                    )
                    return bibtex
            except Exception as e:
                self.logger.error(
                    f"Error with {fetcher.__class__.__name__}: {str(e)}"
                )
                continue

        self.logger.warning(f"No citation found for: {query}")
        return None

    def get_multiple_bibtex(
        self, 
        queries: List[str],
        stop_on_first: bool = True
    ) -> Dict[str, Dict[str, str]]:
        """
        Get BibTeX citations for multiple queries using all configured fetchers.

        Args:
            queries: List of search queries
            stop_on_first: If True, stop searching once a citation is found

        Returns:
            Dict[str, Dict[str, str]]: Dictionary mapping queries to results from each fetcher
        """
        results: Dict[str, Dict[str, str]] = {
            query: {} for query in queries
        }
        
        for query in tqdm(queries, desc="Processing queries"):
            for fetcher in self.fetchers:
                fetcher_name = fetcher.__class__.__name__
                
                try:
                    if stop_on_first and any(results[query].values()):
                        continue
                        
                    bibtex = fetcher.get_bibtex(query)
                    if bibtex:
                        results[query][fetcher_name] = bibtex
                        
                except Exception as e:
                    self.logger.error(
                        f"Error with {fetcher_name} for {query}: {str(e)}"
                    )
                    continue

        return results

    def process_file(
        self, 
        input_path: str, 
        output_path: str,
        stop_on_first: bool = True
    ) -> bool:
        """
        Process queries from a file and save results.

        Args:
            input_path: Path to input file containing queries
            output_path: Path to save results
            stop_on_first: If True, stop searching once a citation is found

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Read input file
            input_file = Path(input_path)
            if not input_file.exists():
                raise FileNotFoundError(f"Input file not found: {input_path}")
                
            with open(input_file, 'r', encoding='utf-8') as f:
                queries = [line.strip() for line in f if line.strip()]

            # Get citations
            results = self.get_multiple_bibtex(queries, stop_on_first)

            # Save results
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                for query, fetcher_results in results.items():
                    f.write(f"% Query: {query}\n")
                    if not fetcher_results:
                        f.write("% No citations found\n\n")
                        continue
                        
                    for fetcher_name, bibtex in fetcher_results.items():
                        f.write(f"% Source: {fetcher_name}\n")
                        f.write(f"{bibtex}\n\n")

            # Log statistics
            total = len(queries)
            found = sum(1 for r in results.values() if r)
            self.logger.info(f"Processed {total} queries, found {found} citations")
            
            return True

        except Exception as e:
            self.logger.error(f"Error processing file: {str(e)}")
            return False

    def get_statistics(self) -> Dict[str, Dict[str, int]]:
        """
        Get usage statistics for each fetcher.

        Returns:
            Dict[str, Dict[str, int]]: Statistics for each fetcher
        """
        stats = {}
        for fetcher in self.fetchers:
            name = fetcher.__class__.__name__
            stats[name] = {
                'total_requests': getattr(fetcher, '_request_count', 0),
                'successful_requests': getattr(fetcher, '_success_count', 0),
                'failed_requests': getattr(fetcher, '_error_count', 0)
            }
        return stats
