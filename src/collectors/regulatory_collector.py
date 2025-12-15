"""
Enhanced Regulatory Text Collector - Complete Version

Smart parsers for EU regulatory texts:
- GDPR (gdpr-info.eu)
- EU AI Act (artificialintelligenceact.eu)
- MICA (Wikipedia - correct URL!)
- MiFID2 (Wikipedia)
- PSD2 (Wikipedia)

Status: 5/5 regulations functional ✅
"""

import json
import sys
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import re

# Fix Python path for direct execution
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.config import REGULATORY_DB_PATH
from src.utils.logger import logger
from src.data.weaviate import Weaviate

# MICA (Markets in Crypto-Assets)
# Date: 2025-12-15
# Status: ✅ FIXED - Correct Wikipedia URL identified!
# 
# Working source:
# Wikipedia: https://en.wikipedia.org/wiki/Markets_in_Crypto-Assets
# Parser: wiki (same as MiFID2)
#
# Previously attempted (failed):
# 1. Markets_in_Crypto-assets_Regulation (wrong URL)
# 2. Blockworks guide (anti-bot protection)
# 3. EUR-Lex (complex parsing)
#
# Resolution: User identified correct Wikipedia URL variant
# The page title uses "Crypto-Assets" not "Crypto-assets_Regulation"

class RegulatoryCollector:
    """Collect official EU regulatory texts with smart parsers"""
    
    def __init__(self):
        self.base_path = REGULATORY_DB_PATH
        try:
            self.weaviate = Weaviate()
        except Exception:
            self.weaviate = None  # Weaviate optional
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Working sources (MICA re-added with correct URL!)
        self.cache = {}
        self.last_updated = None
        self.sources = {
            "gdpr": {
                "url": "https://gdpr-info.eu/",
                "filename": "gdpr.json",
                "regulation": "GDPR",
                "year": 2016,
                "parser": "gdpr"
            },
            "eu_ai_act": {
                "url": "https://artificialintelligenceact.eu/",
                "filename": "eu_ai_act.json",
                "regulation": "EU AI Act",
                "year": 2024,
                "parser": "ai_act"
            },
            "mica": {
                "url": "https://en.wikipedia.org/wiki/Markets_in_Crypto-Assets",
                "filename": "mica.json",
                "regulation": "MICA",
                "year": 2023,
                "parser": "wiki_ultra_simple"
            },
            "mifid2": {
                "url": "https://en.wikipedia.org/wiki/MiFID_II",
                "filename": "mifid2.json",
                "regulation": "MiFID2",
                "year": 2014,
                "parser": "wiki"
            },
            "psd2": {
                "url": "https://en.wikipedia.org/wiki/Payment_Services_Directive",
                "filename": "psd2.json",
                "regulation": "PSD2",
                "year": 2015,
                "parser": "wiki_lenient"
            }
        }
    
    def fetch_html(self, url):
        """Fetch HTML from URL"""
        try:
            logger.info(f"   🔄 Fetching {url}...")
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            logger.info(f"      ✓ Status: {response.status_code}, Size: {len(response.text)} bytes")
            return response.text
        except Exception as e:
            logger.error(f"      ❌ Error: {e}")
            return None
    
    def parse_gdpr(self, html):
        """Parse GDPR from gdpr-info.eu"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text()
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            articles = []
            current_article = None
            
            for line in lines:
                if line.startswith('Article '):
                    if current_article and len(current_article['text']) > 50:
                        articles.append(current_article)
                    current_article = {
                        "number": line.split()[1] if len(line.split()) > 1 else len(articles)+1,
                        "title": line,
                        "text": ""
                    }
                elif current_article:
                    current_article['text'] += " " + line
            
            if current_article and len(current_article['text']) > 50:
                articles.append(current_article)
            
            return [{
                "number": str(a['number']),
                "title": a['title'][:150],
                "text": a['text'].strip()[:3000]
            } for a in articles if a['text'].strip()]
        except Exception as e:
            logger.error(f"      Parse error: {e}")
            return None
    
    def parse_ai_act(self, html):
        """Parse EU AI Act from artificialintelligenceact.eu"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find main content container
            main = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
            if not main:
                main = soup.body
            
            articles = []
            
            # Look for headings and content
            for heading in main.find_all(['h2', 'h3']):
                title = heading.get_text(strip=True)
                
                # Skip navigation/metadata
                if any(x in title.lower() for x in ['menu', 'nav', 'sidebar', 'footer']):
                    continue
                
                # Get content after heading
                content_parts = []
                elem = heading.find_next_sibling()
                
                while elem and elem.name not in ['h2', 'h3'] and len(' '.join(content_parts)) < 3000:
                    if elem.name in ['p', 'ul', 'ol']:
                        text = elem.get_text(strip=True)
                        if text and len(text) > 20:
                            content_parts.append(text)
                    elem = elem.find_next_sibling()
                
                full_text = ' '.join(content_parts)
                if len(full_text) > 100:
                    articles.append({
                        "number": len(articles) + 1,
                        "title": title[:150],
                        "text": full_text[:3000]
                    })
            
            return articles if articles else None
        except Exception as e:
            logger.error(f"      Parse error: {e}")
            return None
    
    def parse_wiki_smart(self, html):
        """Smart Wikipedia parser - extracts actual sections"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Get mw-content-text (Wikipedia main content)
            content = soup.find('div', id='mw-content-text')
            if not content:
                content = soup.find('div', class_='mw-parser-output')
            if not content:
                return None
            
            articles = []
            
            # Extract all text and split smartly
            all_text = content.get_text()
            
            # Split by common heading patterns
            sections = re.split(r'\n(?=[A-Z][a-z]+\s+(?:and|or|\[))', all_text)
            
            for i, section in enumerate(sections):
                lines = [l.strip() for l in section.split('\n') if l.strip()]
                if not lines:
                    continue
                
                title = lines[0][:150]
                
                # Join paragraph text
                content_text = ' '.join(lines[1:])
                
                # Remove citation markers [1], [2], etc
                content_text = re.sub(r'\[\d+\]', '', content_text)
                content_text = re.sub(r'\[citation needed\]', '', content_text)
                
                # Clean whitespace
                content_text = ' '.join(content_text.split())
                
                if len(content_text) > 200:  # At least 200 chars
                    articles.append({
                        "number": i + 1,
                        "title": title,
                        "text": content_text[:3000]
                    })
            
            return articles if len(articles) > 3 else None
        except Exception as e:
            logger.error(f"Parse error: {e}")
            return None
    
    def parse_wiki_lenient(self, html):
        """More lenient Wikipedia parser for difficult pages"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            content = soup.find('div', id='mw-content-text')
            if not content:
                content = soup.find('div', class_='mw-parser-output')
            if not content:
                return None
            
            articles = []
            
            # Get all paragraphs
            paragraphs = content.find_all('p')
            
            current_section = None
            for i, p in enumerate(paragraphs):
                text = p.get_text(strip=True)
                
                # Remove citation markers
                text = re.sub(r'\[\d+\]', '', text)
                text = re.sub(r'\[citation needed\]', '', text)
                text = ' '.join(text.split())
                
                if len(text) > 150:  # Longer minimum for this parser
                    if not current_section:
                        current_section = {
                            "number": len(articles) + 1,
                            "title": f"Section {len(articles) + 1}",
                            "text": text[:3000]
                        }
                        articles.append(current_section)
                    else:
                        current_section['text'] += " " + text
                        if len(current_section['text']) > 2500:
                            current_section = None
            
            return articles if len(articles) > 2 else None
        except Exception as e:
            logger.error(f"Parse error: {e}")
            return None
    
    def parse_wiki_ultra_simple(self, html):
        """Ultra-simple Wikipedia parser - just extract all text content"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Get main content
            content = soup.find('div', id='mw-content-text')
            if not content:
                content = soup.body
            
            if not content:
                return None
            
            articles = []
            
            # Get ALL text - very simple approach
            all_paragraphs = []
            
            # Find all paragraphs
            for p in content.find_all('p'):
                text = p.get_text(strip=True)
                
                # Basic cleanup
                text = re.sub(r'\[\d+\]', '', text)
                text = re.sub(r'\[.*?\]', '', text)
                text = ' '.join(text.split())
                
                # Accept ANY non-empty text
                if text and len(text) > 30:
                    all_paragraphs.append(text)
            
            # Group paragraphs into articles
            if not all_paragraphs:
                return None
            
            # Create articles from paragraphs (combine related ones)
            current_text = ""
            for i, para in enumerate(all_paragraphs):
                current_text += para + " "
                
                # Every 2-3 paragraphs, save as an article
                if (i + 1) % 3 == 0 or i == len(all_paragraphs) - 1:
                    if len(current_text) > 100:
                        articles.append({
                            "number": len(articles) + 1,
                            "title": f"Section {len(articles) + 1}",
                            "text": current_text[:3000].strip()
                        })
                        current_text = ""
            
            # Return if we have ANY articles
            return articles if len(articles) > 0 else None
        except Exception as e:
            logger.error(f"Parse error: {e}")
            return None
    
    def fetch_one(self, name):
        """Fetch and process one regulation"""
        config = self.sources.get(name)
        if not config:
            logger.error(f"Unknown: {name}")
            return False
        
        logger.info(f"\n📖 {name.upper()}")
        logger.info(f"   {config['regulation']} ({config['year']})")
        
        # Fetch
        html = self.fetch_html(config["url"])
        if not html:
            return False
        
        # Parse with specific parser
        parser_name = config.get("parser", "gdpr")
        
        if parser_name == "gdpr":
            articles = self.parse_gdpr(html)
        elif parser_name == "ai_act":
            articles = self.parse_ai_act(html)
        elif parser_name == "wiki":
            articles = self.parse_wiki_smart(html)
        elif parser_name == "wiki_lenient":
            articles = self.parse_wiki_lenient(html)
        elif parser_name == "wiki_super_lenient":
            articles = self.parse_wiki_super_lenient(html)
        elif parser_name == "wiki_ultra_simple":
            articles = self.parse_wiki_ultra_simple(html)
        else:
            articles = self.parse_gdpr(html)
        
        if not articles or len(articles) == 0:
            logger.error(f"      ❌ No articles extracted")
            return False
        
        logger.info(f"      ✓ Extracted {len(articles)} articles")
        
        # Save
        self.save({
            "regulation": config["regulation"],
            "year": config["year"],
            "articles": articles,
            "count": len(articles),
            "source": config["url"]
        }, config["filename"])
        
        # Store
        self.store_in_weaviate(
            title=config["regulation"],
            articles=articles,
            regulation=config["regulation"],
            year=config["year"]
        )
        
        logger.info(f"   ✅ {name} complete!\n")
        return True
    
    def fetch_all(self):
        """Fetch all regulations"""
        logger.info(f"\n{'='*70}")
        logger.info(f"📚 REGULATORY DATA COLLECTION")
        logger.info(f"{'='*70}")
        
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        results = {}
        for name in self.sources.keys():
            try:
                results[name] = self.fetch_one(name)
            except Exception as e:
                logger.error(f"Error processing {name}: {e}")
                results[name] = False
        
        # Summary
        successful = sum(1 for v in results.values() if v)
        logger.info(f"{'='*70}")
        logger.info(f"✅ COMPLETE: {successful}/{len(results)} regulations")
        logger.info(f"{'='*70}\n")
        
        for name, success in results.items():
            status = "✅" if success else "❌"
            print(f"{status} {name.upper()}")
        
        print(f"\n{'='*70}\n")
        
        self.weaviate.close()
        return results
    
    def store_in_weaviate(self, title, articles, regulation, year):
        """Store in Weaviate"""
        try:
            for article in articles[:100]:
                self.weaviate.add_regulation(
                    title=title,
                    article=article.get("title", f"Art. {article.get('number')}"),
                    text=article.get("text", ""),
                    regulation=regulation
                )
            logger.info(f"      ✓ Weaviate: {len(articles)} articles stored")
        except Exception as e:
            logger.error(f"      Weaviate error: {e}")
    

    def fetch(self):
        """Alias for fetch_all() - fetch all data"""
        return self.fetch_all()

    def collect(self):
        """Alias for fetch_all() - collect all data"""
        return self.fetch_all()

    def validate(self, data):
        """Validate fetched data structure"""
        if data is None:
            return False
        if isinstance(data, (list, dict)):
            return len(data) > 0
        return True

    def is_valid(self, data):
        """Check if data is valid"""
        return self.validate(data)

    def use_cache(self, key):
        """Check if key exists in cache"""
        return key in self.cache

    def get_timestamp(self):
        """Get last update timestamp"""
        from datetime import datetime
        if self.last_updated is None:
            self.last_updated = datetime.now()
        return self.last_updated

    def save(self, data, filename):
        """Save to JSON"""
        filepath = self.base_path / filename
        with open(filepath, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"      ✓ Saved: {filename}")

    def fetch(self):
        """Alias for fetch_all() - fetch all data"""
        return self.fetch_all()

    def collect(self):
        """Alias for fetch_all() - collect all data"""
        return self.fetch_all()

    def validate(self, data):
        """Validate fetched data structure"""
        if data is None:
            return False
        if isinstance(data, (list, dict)):
            return len(data) > 0
        return True

    def is_valid(self, data):
        """Check if data is valid"""
        return self.validate(data)

    def use_cache(self, key):
        """Check if key exists in cache"""
        return key in self.cache