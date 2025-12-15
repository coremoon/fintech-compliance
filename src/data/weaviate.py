"""
Weaviate Integration - v1.28.0 with v4 API

Local development with API Key authentication and BM25 full-text search.
"""

import weaviate
from weaviate.classes.config import Property, DataType
from weaviate.auth import AuthApiKey
from typing import List, Dict
import time
from src.config import WEAVIATE_URL, WEAVIATE_API_KEY
from src.utils.logger import logger


class Weaviate:
    """Connect to Weaviate v1.28.0 with API Key authentication and BM25 search"""
    
    def __init__(self, url: str = WEAVIATE_URL, api_key: str = WEAVIATE_API_KEY, wait_for_startup: bool = True):
        """Initialize Weaviate client v1.28.0 with API Key
        
        Args:
            url: Weaviate URL (e.g., http://localhost:8090)
            api_key: API key for authentication
            wait_for_startup: Wait for Weaviate to be ready (up to 30 seconds)
        """
        
        # Parse URL
        if url.startswith("http://"):
            url_clean = url.replace("http://", "")
        elif url.startswith("https://"):
            url_clean = url.replace("https://", "")
        else:
            url_clean = url
        
        host, port = url_clean.split(":") if ":" in url_clean else (url_clean, 8090)
        port = int(port)
        
        # Setup auth
        auth = AuthApiKey(api_key=api_key) if api_key else None
        
        # Try to connect with retries
        max_retries = 30
        for attempt in range(max_retries):
            try:
                self.client = weaviate.connect_to_local(
                    host=host,
                    port=port,
                    auth_credentials=auth
                )
                logger.info(f"✅ Connected to Weaviate at {host}:{port} with API Key auth")
                return
                
            except Exception as e:
                if not wait_for_startup or attempt == max_retries - 1:
                    raise ConnectionError(
                        f"Weaviate not running at {host}:{port}\n\n"
                        f"Solution: Make sure Weaviate is running first!\n"
                        f"  Run: docker-compose up -d\n"
                        f"  Then: make weaviate-init\n\n"
                        f"Error: {e}"
                    )
                
                if attempt == 0:
                    logger.warning(f"Weaviate not ready, waiting... (attempt {attempt + 1}/{max_retries})")
                
                time.sleep(1)
    
    def close(self):
        """Close connection"""
        if self.client:
            self.client.close()
    
    def create_schema(self):
        """Create classes for regulations and cases"""
        
        try:
            # Delete existing classes if they exist
            try:
                self.client.collections.delete("Case")
            except:
                pass
            
            try:
                self.client.collections.delete("Regulation")
            except:
                pass
            
            # Create Case class
            self.client.collections.create(
                name="Case",
                description="Enforcement cases",
                properties=[
                    Property(name="company", data_type=DataType.TEXT),
                    Property(name="violation", data_type=DataType.TEXT),
                    Property(name="fine", data_type=DataType.NUMBER),
                    Property(name="articles", data_type=DataType.TEXT_ARRAY),
                    Property(name="year", data_type=DataType.INT),
                    Property(name="lessons", data_type=DataType.TEXT_ARRAY),
                ]
            )
            
            # Create Regulation class
            self.client.collections.create(
                name="Regulation",
                description="EU regulatory articles",
                properties=[
                    Property(name="title", data_type=DataType.TEXT),
                    Property(name="article", data_type=DataType.TEXT),
                    Property(name="text", data_type=DataType.TEXT),
                    Property(name="regulation", data_type=DataType.TEXT),
                ]
            )
            
            logger.info("✅ Schemas created successfully")
        except Exception as e:
            logger.warning(f"Schema creation: {e}")
    
    def add_case(self, company: str, violation: str, fine: float, 
                 articles: List[str], year: int, lessons: List[str]) -> str:
        """Add enforcement case"""
        
        try:
            cases = self.client.collections.get("Case")
            
            uuid = cases.data.insert(
                properties={
                    "company": company,
                    "violation": violation,
                    "fine": fine,
                    "articles": articles,
                    "year": year,
                    "lessons": lessons,
                }
            )
            
            return str(uuid)
        except Exception as e:
            logger.error(f"Error adding case: {e}")
            raise
    
    def add_regulation(self, title: str, article: str, text: str, regulation: str) -> str:
        """Add regulation"""
        
        try:
            regs = self.client.collections.get("Regulation")
            
            uuid = regs.data.insert(
                properties={
                    "title": title,
                    "article": article,
                    "text": text,
                    "regulation": regulation,
                }
            )
            
            return str(uuid)
        except Exception as e:
            logger.error(f"Error adding regulation: {e}")
            raise
    
    def search_cases(self, query: str) -> List[Dict]:
        """Search enforcement cases by violation or company using BM25"""
        
        try:
            cases = self.client.collections.get("Case")
            
            # Use BM25 for full-text search
            results = cases.query.bm25(
                query=query,
                limit=5,
                return_properties=["company", "violation", "fine", "articles", "year", "lessons"]
            )
            
            return [
                {
                    "company": obj.properties.get("company"),
                    "violation": obj.properties.get("violation"),
                    "fine": obj.properties.get("fine"),
                    "articles": obj.properties.get("articles", []),
                    "year": obj.properties.get("year"),
                    "lessons": obj.properties.get("lessons", [])
                }
                for obj in results.objects
            ]
        except Exception as e:
            logger.error(f"Error searching cases: {e}")
            return []
    
    def search_regulations(self, query: str) -> List[Dict]:
        """Search regulations by title, article, or text using BM25"""
        
        try:
            regs = self.client.collections.get("Regulation")
            
            # Use BM25 for full-text search
            results = regs.query.bm25(
                query=query,
                limit=5,
                return_properties=["title", "article", "text", "regulation"]
            )
            
            return [
                {
                    "title": obj.properties.get("title"),
                    "article": obj.properties.get("article"),
                    "text": obj.properties.get("text"),
                    "regulation": obj.properties.get("regulation"),
                }
                for obj in results.objects
            ]
        except Exception as e:
            logger.error(f"Error searching regulations: {e}")
            return []
    
    def get_all_cases(self) -> List[Dict]:
        """Get all cases"""
        
        try:
            cases = self.client.collections.get("Case")
            
            results = cases.query.fetch_objects(limit=100)
            
            return [
                {
                    "company": obj.properties.get("company"),
                    "violation": obj.properties.get("violation"),
                    "fine": obj.properties.get("fine"),
                    "articles": obj.properties.get("articles", []),
                    "year": obj.properties.get("year"),
                    "lessons": obj.properties.get("lessons", [])
                }
                for obj in results.objects
            ]
        except Exception as e:
            logger.error(f"Error getting cases: {e}")
            return []
    
    def get_all_regulations(self) -> List[Dict]:
        """Get all regulations"""
        
        try:
            regs = self.client.collections.get("Regulation")
            
            results = regs.query.fetch_objects(limit=100)
            
            return [
                {
                    "title": obj.properties.get("title"),
                    "article": obj.properties.get("article"),
                    "text": obj.properties.get("text"),
                    "regulation": obj.properties.get("regulation"),
                }
                for obj in results.objects
            ]
        except Exception as e:
            logger.error(f"Error getting regulations: {e}")
            return []


# Usage example
if __name__ == "__main__":
    w = Weaviate()
    w.create_schema()
    print("✅ Weaviate ready")
    w.close()
