import requests
from bs4 import BeautifulSoup
import re
import json
import os
from datetime import datetime

class TelegramScraper:
    def __init__(self, channels):
        self.channels = channels

    def fetch_latest_messages(self, channel_id):
        url = f"https://t.me/s/{channel_id}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                print(f"Error: {channel_id} returned status {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            print(f"DEBUG: Response length for {channel_id}: {len(response.text)}")
            if "Robot Check" in response.text or "Captcha" in response.text:
                print(f"DEBUG: Blocked by bot check on {channel_id}")
            
            messages = []
            
            # Broader search for message-like containers
            msg_elements = soup.find_all('div', class_=re.compile(r'tgme_widget_message'))
            print(f"DEBUG: Found {len(msg_elements)} message elements in @{channel_id}")
            
            for el in msg_elements:
                text_el = el.find('div', class_='tgme_widget_message_text')
                if not text_el:
                    continue
                    
                text = text_el.get_text(separator='\n')
                # Try to find links/PDFs
                links = [a['href'] for a in el.find_all('a', href=True) if 't.me/iv' not in a['href']]
                
                messages.append({
                    "source": f"Telegram: @{channel_id}",
                    "text": text,
                    "links": links,
                    "timestamp": datetime.now().isoformat()
                })
            return messages
        except Exception as e:
            print(f"Error fetching {channel_id}: {e}")
            return []

    def scan_all(self):
        all_signals = []
        for channel in self.channels:
            all_signals.extend(self.fetch_latest_messages(channel))
        return all_signals

class PDFProcessor:
    @staticmethod
    def extract_text(pdf_path):
        try:
            import fitz # PyMuPDF
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except Exception as e:
            return f"PDF Error: {e}"

    @staticmethod
    def download_pdf(url, dest_dir="/tmp/lor_pdfs"):
        os.makedirs(dest_dir, exist_ok=True)
        local_filename = os.path.join(dest_dir, url.split('/')[-1])
        if not local_filename.endswith('.pdf'):
            local_filename += ".pdf"
            
        try:
            with requests.get(url, stream=True, timeout=30) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return local_filename
        except Exception as e:
            print(f"Download failed {url}: {e}")
            return None

def main():
    # Example Scan
    CHANNELS = ["JKUpdates"]
    scraper = TelegramScraper(CHANNELS)
    signals = scraper.scan_all()
    
    # Filter for signals that look like opportunities (keyword check)
    keywords = ["recruitment", "job", "notice", "tender", "post", "vacancy", "hiring"]
    opportunities = []
    
    for s in signals:
        if any(k in s['text'].lower() for k in keywords):
            opportunities.append(s)
            
    print(f"Found {len(opportunities)} potential signals in Telegram.")
    if opportunities:
        print(json.dumps(opportunities[0], indent=2))

if __name__ == "__main__":
    main()
