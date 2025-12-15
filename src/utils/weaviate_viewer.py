#!/usr/bin/env python3
"""
🔍 WEAVIATE VIEWER - Interactive Data Browser

View all regulatory articles and enforcement cases in Weaviate
"""

import requests
import json
import sys
from typing import List, Dict, Any

class WeaviateViewer:
    """Interactive Weaviate data viewer"""
    
    def __init__(self, url="http://localhost:8098", api_key="W3aviate"):
        self.url = url
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        self.all_data = []
        
    def query(self, query_str: str) -> Dict[str, Any]:
        """Execute GraphQL query"""
        try:
            response = requests.post(
                f"{self.url}/v1/graphql",
                json={"query": query_str},
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"❌ HTTP {response.status_code}")
                return {}
            
            data = response.json()
            
            if isinstance(data, dict) and 'errors' in data:
                print(f"❌ GraphQL Error: {data['errors']}")
                return {}
            
            return data.get('data', {}) if isinstance(data, dict) else {}
        except Exception as e:
            print(f"❌ Error: {e}")
            return {}
    
    def fetch_all_data(self) -> bool:
        """Fetch all data from Weaviate"""
        print("\n📡 Connecting to Weaviate...\n")
        
        # Get stats
        stats_query = """
        {
          Aggregate {
            Regulation {
              meta { count }
            }
            Case {
              meta { count }
            }
          }
        }
        """
        
        stats = self.query(stats_query)
        
        if not stats or 'Aggregate' not in stats:
            print("❌ Failed to get stats")
            return False
        
        agg = stats['Aggregate']
        
        # Parse counts (handle list format)
        reg_count = 0
        case_count = 0
        
        if 'Regulation' in agg:
            reg_data = agg['Regulation']
            if isinstance(reg_data, list) and len(reg_data) > 0:
                reg_count = reg_data[0].get('meta', {}).get('count', 0)
            elif isinstance(reg_data, dict):
                reg_count = reg_data.get('meta', {}).get('count', 0)
        
        if 'Case' in agg:
            case_data = agg['Case']
            if isinstance(case_data, list) and len(case_data) > 0:
                case_count = case_data[0].get('meta', {}).get('count', 0)
            elif isinstance(case_data, dict):
                case_count = case_data.get('meta', {}).get('count', 0)
        
        print(f"✅ Connected!")
        print(f"   Regulations: {reg_count}")
        print(f"   Cases: {case_count}\n")
        
        # Fetch regulations in batches
        if reg_count > 0:
            batch_size = 100
            for offset in range(0, min(reg_count, 1000), batch_size):
                limit = min(batch_size, reg_count - offset)
                
                reg_query = f"""
                {{
                  Get {{
                    Regulation(limit: {limit} offset: {offset}) {{
                      title
                      regulation
                      article
                      text
                      _additional {{ id }}
                    }}
                  }}
                }}
                """
                
                data = self.query(reg_query)
                if 'Get' in data and 'Regulation' in data['Get']:
                    regulations = data['Get']['Regulation']
                    
                    for reg in regulations:
                        self.all_data.append({
                            'type': 'Regulation',
                            'title': reg.get('title', 'Unknown'),
                            'regulation': reg.get('regulation', 'Unknown'),
                            'article': reg.get('article', ''),
                            'text': reg.get('text', '')[:200],
                            'id': reg.get('_additional', {}).get('id', '')
                        })
        
        # Fetch cases in batches
        if case_count > 0:
            # Note: Cases are actually stored in Regulation collection as "Enforcement: XXX"
            # So we skip fetching from Case collection
            pass  # All cases already in Regulation collection
        
        print(f"✅ Loaded {len(self.all_data)} items\n")
        return len(self.all_data) > 0
    
    def display_all(self):
        """Display all data organized by type"""
        if not self.all_data:
            print("❌ No data loaded")
            return
        
        print(f"\n{'='*80}")
        print(f"📚 WEAVIATE DATA - {len(self.all_data)} ITEMS")
        print(f"{'='*80}\n")
        
        by_reg = {}
        for item in self.all_data:
            reg = item['regulation']
            if reg not in by_reg:
                by_reg[reg] = []
            by_reg[reg].append(item)
        
        for reg in sorted(by_reg.keys()):
            items = by_reg[reg]
            print(f"\n{'─'*80}")
            print(f"📌 {reg} ({len(items)} items)")
            print(f"{'─'*80}")
            
            for i, item in enumerate(items[:5], 1):
                icon = "📋" if item['type'] == "Case" else "📚"
                print(f"{i}. {icon} {item['title']}")
                if item.get('text'):
                    print(f"   {item['text']}...")
            
            if len(items) > 5:
                print(f"   ... and {len(items)-5} more")
        
        print(f"\n{'='*80}\n")
    
    def search(self, query_term: str) -> List[Dict]:
        """Search for items"""
        results = []
        query_lower = query_term.lower()
        
        for item in self.all_data:
            if (query_lower in item.get('title', '').lower() or
                query_lower in item.get('regulation', '').lower() or
                query_lower in item.get('article', '').lower() or
                query_lower in item.get('text', '').lower()):
                results.append(item)
        
        return results
    
    def display_search(self, results: List[Dict], query_term: str):
        """Display search results"""
        if not results:
            print(f"\n❌ No results for '{query_term}'")
            return
        
        print(f"\n{'='*80}")
        print(f"🔍 SEARCH: '{query_term}' ({len(results)} found)")
        print(f"{'='*80}\n")
        
        for i, item in enumerate(results[:20], 1):
            icon = "📋" if item['type'] == "Case" else "📚"
            print(f"{i}. {icon} {item['title']}")
            print(f"   {item['regulation']}")
            print()
        
        if len(results) > 20:
            print(f"... and {len(results)-20} more\n")
    
    def display_by_type(self, item_type: str):
        """Display only one type"""
        items = [item for item in self.all_data if item['type'] == item_type]
        
        if not items:
            print(f"\n❌ No {item_type} items")
            return
        
        icon = "📋" if item_type == "Case" else "📚"
        print(f"\n{'='*80}")
        print(f"{icon} {item_type.upper()} ({len(items)} items)")
        print(f"{'='*80}\n")
        
        for i, item in enumerate(items[:20], 1):
            print(f"{i}. {item['title']}")
            print(f"   {item['regulation']}")
            print()
        
        if len(items) > 20:
            print(f"... and {len(items)-20} more\n")
    
    def export_json(self, filename: str = "weaviate_export.json"):
        """Export to JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.all_data, f, indent=2)
            print(f"\n✅ Exported {len(self.all_data)} items to {filename}\n")
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
    
    def show_summary(self):
        """Show summary"""
        if not self.all_data:
            print("❌ No data")
            return
        
        print(f"\n{'='*80}")
        print(f"📊 SUMMARY")
        print(f"{'='*80}\n")
        
        by_type = {}
        by_reg = {}
        
        for item in self.all_data:
            t = item['type']
            by_type[t] = by_type.get(t, 0) + 1
            
            r = item['regulation']
            by_reg[r] = by_reg.get(r, 0) + 1
        
        print("BY TYPE:")
        for t in sorted(by_type.keys()):
            print(f"   {t:20s}: {by_type[t]:5d}")
        
        print(f"\nBY REGULATION:")
        for r in sorted(by_reg.keys())[:10]:
            print(f"   {r:40s}: {by_reg[r]:5d}")
        
        if len(by_reg) > 10:
            print(f"   ... and {len(by_reg)-10} more")
        
        print(f"\nTOTAL: {len(self.all_data)} items")
        print(f"{'='*80}\n")

def main():
    viewer = WeaviateViewer()
    
    if not viewer.fetch_all_data():
        print("❌ Failed to connect or fetch data")
        sys.exit(1)
    
    viewer.show_summary()
    
    while True:
        print("\n🔍 MENU")
        print("─" * 80)
        print("1. View all (organized)")
        print("2. View regulations only")
        print("3. View cases only")
        print("4. Search")
        print("5. Summary")
        print("6. Export JSON")
        print("7. Exit")
        print("─" * 80)
        
        choice = input("\nSelect (1-7): ").strip()
        
        if choice == "1":
            viewer.display_all()
        elif choice == "2":
            viewer.display_by_type("Regulation")
        elif choice == "3":
            viewer.display_by_type("Case")
        elif choice == "4":
            query = input("Search: ").strip()
            if query:
                viewer.display_search(viewer.search(query), query)
        elif choice == "5":
            viewer.show_summary()
        elif choice == "6":
            fn = input("Filename (default: weaviate_export.json): ").strip()
            viewer.export_json(fn or "weaviate_export.json")
        elif choice == "7":
            print("\n✅ Goodbye!\n")
            break
        else:
            print("❌ Invalid")

if __name__ == "__main__":
    main()
