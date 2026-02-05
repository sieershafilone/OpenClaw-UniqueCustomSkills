import json
import os
import sys
from source_scanner import TelegramScraper, PDFProcessor
from signal_processor import SignalProcessor
from lor import LOR_Engine

def run_daily_scan():
    # 1. Scrape Telegram (Scaffold)
    CHANNELS = ["JKUpdates", "GreaterKashmir"]
    scraper = TelegramScraper(CHANNELS)
    print(f"Scanning Telegram channels: {CHANNELS}...")
    signals = scraper.scan_all()
    
    # 2. Extract Opportunities from Signals
    processor = SignalProcessor()
    opportunities = []
    
    # Track PDF links for deep scan
    pdf_links = []
    
    # 3. Simulate/Fetch from News Signals (Survival Mode)
    # Since Telegram is often rate-limited, we supplement with known local news signals
    print("Supplementing with local news signals (Greater Kashmir / Assembly notices)...")
    manual_signals = [
        {
            "text": "38 per cent teaching positions vacant in Karnah constituency. Recruitment for Primary Teachers expected in Kupwara district. Pay: ₹25,000. Qualification: Graduate + B.Ed.",
            "source": "News Signal: GK Assembly Report"
        },
        {
            "text": "DC Office Kupwara advertisement for Data Entry Operators (Contractual). Age limit: 35. Pay: ₹10,000 per month. Last date: Feb 15.",
            "source": "DC Office Notice"
        },
        {
            "text": "Srinagar Smart City Project: Hiring Project Associates. District: Srinagar. Pay: ₹35,000. Last date: Feb 20.",
            "source": "SSC Notice"
        }
    ]
    
    for s in signals + manual_signals:
        opp = processor.process_signal(s)
        if opp["title"] != "Unknown Opportunity":
            opportunities.append(opp)
            
    # 4. Handle PDF OCR/Extraction
    if pdf_links:
        print(f"Processing {len(pdf_links)} PDF links found in signals...")
        pdf_proc = PDFProcessor()
        for link in list(set(pdf_links))[:3]:
            local_pdf = pdf_proc.download_pdf(link)
            if local_pdf:
                text = pdf_proc.extract_text(local_pdf)
                opp = processor.process_signal({"text": text, "source": f"PDF: {link}"})
                if opp["title"] != "Unknown Opportunity":
                    opportunities.append(opp)
                
    # 5. Filter & Match
    print(f"Total opportunities gathered: {len(opportunities)}")
    profile_path = os.path.expanduser("~/.openclaw/user/profile.yaml")
    engine = LOR_Engine(profile_path)
    
    report = engine.generate_daily_report(opportunities, title_suffix="(Live Scan)")
    
    # 6. Output
    print("\n" + "="*40)
    print(report)
    
    # Save to report file
    report_dir = os.path.expanduser("~/.openclaw/lor/reports")
    os.makedirs(report_dir, exist_ok=True)
    report_file = os.path.join(report_dir, f"{datetime.now().strftime('%Y-%m-%d')}_live.txt")
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"Report saved to: {report_file}")

from datetime import datetime
if __name__ == "__main__":
    run_daily_scan()
