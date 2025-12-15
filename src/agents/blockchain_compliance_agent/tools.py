"""
Compliance Advisor Tools - Weaviate Integration

Provides tools for:
- Searching regulations
- Retrieving enforcement cases
- Analyzing compliance risks
"""

import requests
import json
from typing import List, Dict, Any
from src.utils.logger import logger


class ComplianceTools:
    """Tools for compliance analysis and Weaviate interaction"""
    
    def __init__(self, weaviate_url: str = "http://localhost:8098", 
                 api_key: str = "W3aviate"):
        """
        Initialize compliance tools
        
        Args:
            weaviate_url: Weaviate instance URL
            api_key: Weaviate API authentication key
        """
        self.url = weaviate_url
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    
    def search_regulations(self, query: str, 
                          regulation: str = None) -> List[Dict[str, Any]]:
        """
        Search regulatory documents by keyword
        
        Args:
            query: Search term (e.g., "data protection", "cryptocurrency")
            regulation: Specific regulation filter (e.g., "GDPR", "MICA")
        
        Returns:
            List of matching regulatory articles
        """
        
        where_filter = None
        if regulation and not regulation.startswith("Enforcement"):
            where_filter = {
                "path": ["regulation"],
                "operator": "Equal",
                "valueString": regulation
            }
        
        gql_query = f"""
        {{
          Get {{
            Regulation(
              limit: 10
              where: {json.dumps(where_filter) if where_filter else "null"}
            ) {{
              title
              regulation
              article
              text
              _additional {{ distance }}
            }}
          }}
        }}
        """
        
        try:
            response = requests.post(
                f"{self.url}/v1/graphql",
                json={"query": gql_query},
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'Get' in data['data']:
                    return data['data']['Get'].get('Regulation', [])
        except Exception as e:
            logger.error(f"Search error: {e}")
        
        return []
    
    def get_enforcement_cases(self, query: str = None) -> List[Dict[str, Any]]:
        """
        Retrieve enforcement cases from Weaviate
        
        Args:
            query: Optional search term (e.g., "Kraken", "Celsius")
        
        Returns:
            List of enforcement cases
        """
        
        gql_query = """
        {
          Get {
            Regulation(limit: 100) {
              title
              regulation
              article
              text
              _additional { id }
            }
          }
        }
        """
        
        try:
            response = requests.post(
                f"{self.url}/v1/graphql",
                json={"query": gql_query},
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'Get' in data['data']:
                    all_items = data['data']['Get'].get('Regulation', [])
                    
                    # Filter for enforcement cases
                    cases = [
                        item for item in all_items 
                        if 'Enforcement' in item.get('regulation', '')
                    ]
                    
                    # Optional search filter
                    if query:
                        cases = [
                            case for case in cases
                            if query.lower() in case.get('title', '').lower()
                            or query.lower() in case.get('article', '').lower()
                        ]
                    
                    return cases
        except Exception as e:
            logger.error(f"Enforcement cases retrieval error: {e}")
        
        return []
    
    def analyze_regulation_coverage(self, 
                                   project_description: str) -> Dict[str, Any]:
        """
        Analyze which regulations are relevant to project
        
        Args:
            project_description: Project description text
        
        Returns:
            Dictionary mapping regulations to relevant articles
        """
        
        regulations = ["GDPR", "MICA", "MiFID2", "PSD2", "EU AI Act"]
        relevant = {}
        
        for reg in regulations:
            articles = self.search_regulations(project_description, reg)
            if articles:
                relevant[reg] = {
                    "count": len(articles),
                    "articles": articles[:3]  # Top 3
                }
        
        return relevant
    
    def get_regulation_summary(self, regulation: str) -> Dict[str, Any]:
        """
        Get summary of specific regulation
        
        Args:
            regulation: Regulation name (e.g., "GDPR")
        
        Returns:
            Regulation overview
        """
        
        articles = self.search_regulations("", regulation)
        
        return {
            "regulation": regulation,
            "total_articles": len(articles),
            "articles": [
                {
                    "title": a.get('title', ''),
                    "article": a.get('article', ''),
                    "text": a.get('text', '')[:200]
                }
                for a in articles[:5]
            ]
        }
    
    def check_enforcement_precedents(self, 
                                    violation_type: str) -> List[Dict[str, Any]]:
        """
        Check for similar enforcement precedents
        
        Args:
            violation_type: Type of violation (e.g., "Unregistered securities")
        
        Returns:
            List of similar enforcement cases
        """
        
        return self.get_enforcement_cases(violation_type)
    
    def get_all_regulations_list(self) -> Dict[str, int]:
        """
        List all available regulations with article counts
        
        Returns:
            Dictionary of regulations and article counts
        """
        
        # Known regulations with manual counts
        return {
            "GDPR": 156,
            "MiFID2": 78,
            "EU AI Act": 42,
            "PSD2": 36,
            "MICA": 15,
            "Enforcement: CFTC": 2,
            "Enforcement: SEC": 2,
            "Enforcement: FCA": 2,
            "Enforcement: CNIL": 2,
            "Enforcement: BaFin": 2
        }
