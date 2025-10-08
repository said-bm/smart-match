from services.facet_parser import FacetParser
import config as cfg
from typing import Dict, Any


class Controller:
    """Controller for managing facet parsing operations"""
    
    def __init__(self):
        self.parser = FacetParser(
            openai_api_key=cfg.OPENAI_API_KEY,
            model_name=cfg.OPENAI_MODEL
        )

    def parse_query(self, query: str) -> Dict[str, Any]:
        """
        Parse a natural language query into structured facets
        
        Args:
            query: User's natural language query
            
        Returns:
            Dictionary containing extracted facets
        """
        return self.parser.parse_query(query)
    
    def parse_query_with_metadata(self, query: str) -> Dict[str, Any]:
        """
        Parse query and return with additional metadata
        
        Args:
            query: User's natural language query
            
        Returns:
            Dictionary with facets and metadata
        """
        return self.parser.parse_query_with_metadata(query)