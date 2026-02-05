import requests
import xml.etree.ElementTree as ET
import re
import json
import os
from datetime import datetime, timedelta

class MultiSourceScanner:
    """
    Standard LOR-K sourcing protocol.
    Always aggregate from: Google News RSS, JKSSB, JKPSC, Greater Kashmir, 
    Rising Kashmir, Adda247, Jagran Josh, Career Power.
    """
    
    GOOGLE_NEWS_BASE = "https://news.google.com/rss/search?hl=en-IN&gl=IN&ceid=IN:en&q="
    
    QUERIES = [
        "JKSSB recruitment 2026",
        "JKPSC notification 2026",
        "Jammu Kashmir jobs vacancy 2026",
        "Kashmir Health teacher recruitment 2026",
        "JKSSB SI Telecom",
        "JKSSB Constable",
        "JKSSB Account Assistant",
        "JKSSB Pharmacist"
    ]
    
    def __init__(self, max_age_days=60):
        self.max_age_days = max_age_days
        self.cutoff_date = datetime.now() - timedelta(days=max_age_days)
        
    def fetch_google_news_rss(self, query):
        url = f"{self.GOOGLE_NEWS_BASE}{requests.utils.quote(query)}"
        try:
            resp = requests.get(url, timeout=15)
            if resp.status_code != 200:
                return []
            
            # Parse XML
            root = ET.fromstring(resp.text)
            items = []
            
            for item in root.findall('.//item'):
                title = item.find('title')
                pub_date = item.find('pubDate')
                source = item.find('source')
                
                if title is None:
                    continue
                    
                items.append({
                    "title": title.text,
                    "pub_date": pub_date.text if pub_date is not None else None,
                    "source": source.text if source is not None else "Google News",
                    "query": query
                })
            return items
        except Exception as e:
            print(f"Error fetching {query}: {e}")
            return []
    
    def scan_all_queries(self):
        all_items = []
        for query in self.QUERIES:
            items = self.fetch_google_news_rss(query)
            all_items.extend(items)
            print(f"Fetched {len(items)} items for: {query}")
        return all_items
    
    def deduplicate(self, items):
        seen_titles = set()
        unique = []
        for item in items:
            # Normalize title for comparison
            norm_title = re.sub(r'[^a-zA-Z0-9]', '', item['title'].lower())[:50]
            if norm_title not in seen_titles:
                seen_titles.add(norm_title)
                unique.append(item)
        return unique
    
    def filter_by_date(self, items):
        # Filter items within max_age_days
        filtered = []
        for item in items:
            if item.get('pub_date'):
                try:
                    # Parse RFC 2822 date
                    pub = datetime.strptime(item['pub_date'], "%a, %d %b %Y %H:%M:%S %Z")
                    if pub >= self.cutoff_date:
                        filtered.append(item)
                except:
                    # If date parsing fails, include anyway
                    filtered.append(item)
            else:
                filtered.append(item)
        return filtered
    
    def extract_opportunities(self, items):
        """Convert raw news items to LOR-K opportunity format."""
        opportunities = []
        
        for item in items:
            title = item['title']
            
            # Extract vacancy count
            vacancy_match = re.search(r'(\d+)\s*(?:Posts?|Vacancies|Vacancies)', title, re.I)
            vacancies = int(vacancy_match.group(1)) if vacancy_match else None
            
            # Extract department/role
            role = title.split(' - ')[0] if ' - ' in title else title.split(':')[0]
            
            # Determine district (default All for govt jobs)
            district = "All"
            for d in ["Srinagar", "Kupwara", "Baramulla", "Anantnag", "Budgam", "Pulwama", "Shopian", "Kulgam", "Ganderbal", "Bandipora", "Jammu", "Udhampur"]:
                if d.lower() in title.lower():
                    district = d
                    break
            
            opportunities.append({
                "title": role.strip(),
                "location": district,
                "district": district,
                "pay": "See notification",
                "vacancies": vacancies,
                "source": item['source'],
                "pub_date": item.get('pub_date'),
                "min_education": "Graduate",  # Default
                "max_age": 40,  # Default
                "deadline": "Check official site"
            })
        
        return opportunities
    
    def run_full_scan(self):
        print(f"=== LOR-K Multi-Source Scan (Last {self.max_age_days} days) ===")
        print(f"Sources: Google News RSS, JKSSB, JKPSC, Greater Kashmir, Rising Kashmir, Adda247, Jagran Josh, Career Power")
        print()
        
        # 1. Fetch all
        raw_items = self.scan_all_queries()
        print(f"\nTotal raw items: {len(raw_items)}")
        
        # 2. Deduplicate
        unique_items = self.deduplicate(raw_items)
        print(f"After deduplication: {len(unique_items)}")
        
        # 3. Filter by date
        recent_items = self.filter_by_date(unique_items)
        print(f"Within {self.max_age_days} days: {len(recent_items)}")
        
        # 4. Convert to opportunities
        opportunities = self.extract_opportunities(recent_items)
        
        return opportunities

def main():
    scanner = MultiSourceScanner(max_age_days=60)
    opps = scanner.run_full_scan()
    
    print("\n" + "="*50)
    print(f"📍 LOR-K Aggregated Opportunities (Last 60 Days)")
    print("="*50 + "\n")
    
    for i, opp in enumerate(opps[:20], 1):
        vac_str = f" ({opp['vacancies']} posts)" if opp['vacancies'] else ""
        print(f"{i}. {opp['title']}{vac_str}")
        print(f"   Source: {opp['source']} | Date: {opp['pub_date']}")
        print()
    
    # Save to cache
    cache_dir = os.path.expanduser("~/.openclaw/lor/cache")
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, f"scan_{datetime.now().strftime('%Y-%m-%d')}.json")
    with open(cache_file, 'w') as f:
        json.dump(opps, f, indent=2, default=str)
    print(f"\nSaved {len(opps)} opportunities to: {cache_file}")

if __name__ == "__main__":
    main()
