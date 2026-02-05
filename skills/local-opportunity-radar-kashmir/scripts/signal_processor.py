import json
import os
import re

class SignalProcessor:
    def __init__(self, model_hook=None):
        self.model_hook = model_hook

    def process_signal(self, signal):
        """
        Converts a raw signal (Telegram text/link) into a structured LOR-K opportunity.
        """
        text = signal.get("text", "")
        
        # Expanded heuristic logic for real Kashmir signals
        opportunity = {
            "title": "Unknown Opportunity",
            "location": "Kashmir",
            "district": "All",
            "pay": "Unspecified",
            "min_education": "10th",
            "max_age": 45,
            "deadline": "Unspecified",
            "raw_source": signal.get("source", "Unknown")
        }
        
        # Improved Title Extraction
        title_patterns = [
            r"(?:Post of|Recruitment for|Hiring|Vacancy for|engagement of|engagement for|advertisement for)\s+([^.\n,]+)",
            r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Posts|Vacancies|Jobs|Recruitment))",
            r"(?:ADVERTISEMENT NOTICE)\s*:?\s*([^.\n]+)"
        ]
        for pattern in title_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                opportunity["title"] = match.group(1).strip()
                break
            
        # Pay Extraction
        pay_match = re.search(r"(?:Pay|Salary|Stipend|₹|Rs\.?)\s*:?\s*([\d,]+(?:/month|/-)?)", text, re.I)
        if pay_match:
            val = pay_match.group(1).strip()
            opportunity["pay"] = f"₹{val}" if '₹' not in val and 'Rs' not in val else val
            
        # District/Location Extraction
        loc_patterns = [
            r"(Kupwara|Handwara|Srinagar|Baramulla|Anantnag|Budgam|Ganderbal|Bandipora|Pulwama|Shopian|Kulgam)",
            r"District\s+([^.\n,]+)"
        ]
        for pattern in loc_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                opportunity["district"] = match.group(1).strip().capitalize()
                opportunity["location"] = match.group(1).strip().capitalize()
                break

        # Qualification
        qual_match = re.search(r"(?:Qual|Education|Eligibility|Qualification)\s*:?\s*([^.\n]+)", text, re.I)
        if qual_match:
             q = qual_match.group(1).lower()
             if "grad" in q or "degree" in q:
                 opportunity["min_education"] = "Graduate"
             elif "12" in q:
                 opportunity["min_education"] = "12th"
             elif "post" in q or "master" in q:
                 opportunity["min_education"] = "Post-Graduate"

        return opportunity

if __name__ == "__main__":
    # Test with a mock raw signal
    mock_signal = {
        "source": "Telegram: @JKUpdates",
        "text": "Recruitment for Field Enumerator in Handwara. Pay: 12000 per month. Last date: 10th Feb. Qual: Graduate.",
        "timestamp": "2026-02-05T16:50:00"
    }
    processor = SignalProcessor()
    opp = processor.process_signal(mock_signal)
    print(json.dumps(opp, indent=2))
