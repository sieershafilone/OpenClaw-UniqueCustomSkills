import yaml
import os
import json
from datetime import datetime

class LOR_Engine:
    def __init__(self, user_profile_path):
        self.profile = self._load_profile(user_profile_path)
        
    def _load_profile(self, path):
        # Mock profile if not exists
        if not os.path.exists(path):
            default_profile = {
                "name": "syer",
                "district": "Kupwara",
                "education": "Graduate",
                "age": 24,
                "skills": ["python", "data-entry", "coordination"],
                "category": "General"
            }
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                yaml.dump(default_profile, f)
            return default_profile
        
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def calculate_eligibility(self, opportunity):
        score = 1.0
        reasons = []
        status = "✅ Eligible"

        # Check District
        user_dist = self.profile.get("district", "All")
        opp_dist = opportunity.get("district", "All")
        
        if user_dist != "All" and opp_dist != user_dist and opp_dist != "All":
            return None # Hard filter

        # Check Age
        if self.profile["age"] > opportunity.get("max_age", 40):
            return None # Hard filter

        # Check Education (Simplified)
        edu_rank = {"10th": 1, "12th": 2, "Graduate": 3, "Post-Graduate": 4}
        req_edu = opportunity.get("min_education", "10th")
        if edu_rank.get(self.profile["education"], 0) < edu_rank.get(req_edu, 0):
            return None # Hard filter

        # Penalty for lack of specific skills if mentioned
        req_skills = opportunity.get("required_skills", [])
        if req_skills:
            match_count = sum(1 for s in req_skills if s.lower() in [p.lower() for p in self.profile.get("skills", [])])
            skill_score = match_count / len(req_skills)
            score *= (0.5 + 0.5 * skill_score)

        # Borderline checks
        if "Action Needed" in opportunity:
            status = "⚠️ Borderline"
            reasons.append(opportunity["Action Needed"])
            score *= 0.8

        # Alert Threshold Check
        if score < 0.65: # default alert_threshold
             status = "❌ Low Match"
             if self.profile.get("hide_ineligible", True):
                 return None

        return {
            "title": opportunity["title"],
            "location": opportunity["location"],
            "pay": opportunity["pay"],
            "deadline": opportunity["deadline"],
            "status": status,
            "reasons": reasons,
            "score": round(score, 2),
            "confidence": "High" if score > 0.8 else "Medium"
        }

    def generate_daily_report(self, opportunities, title_suffix=""):
        eligible_list = []
        for opp in opportunities:
            res = self.calculate_eligibility(opp)
            if res:
                eligible_list.append(res)
        
        # Sort by Pay or Deadline
        # Since Pay is a string "₹12,000", we need to extract the number for sorting
        def get_pay_val(x):
            try:
                return int(re.sub(r'[^\d]', '', x['pay']))
            except:
                return 0

        eligible_list.sort(key=get_pay_val, reverse=True)
        
        output = f"📍 Local Opportunity Radar — {datetime.now().strftime('%Y-%m-%d')} {title_suffix}\n"
        output += f"District: {self.profile['district']} | Profile Match: Strong\n\n"
        
        if not eligible_list:
            output += "No eligible opportunities found for your profile today. Check back tomorrow.\n"
            return output

        for i, opp in enumerate(eligible_list[:7], 1):
            output += f"{opp['status']} Opportunity {i}: {opp['title']}\n"
            output += f"Location: {opp['location']}\n"
            output += f"Pay: {opp['pay']}\n"
            output += f"Deadline: {opp['deadline']}\n"
            if opp['reasons']:
                output += f"Action Needed: {', '.join(opp['reasons'])}\n"
            output += f"Score: {opp['score']} | Confidence: {opp['confidence']}\n\n"
            
        return output

def main():
    # Mock Database of Opportunities (from PDF/WhatsApp/JKSSB)
    mock_db = [
        {
            "title": "NGO Field Enumerator",
            "location": "Handwara",
            "district": "Kupwara",
            "pay": "₹12,000/month",
            "min_education": "Graduate",
            "max_age": 30,
            "deadline": "3 days"
        },
        {
            "title": "Panchayat Contract Work (Data Entry)",
            "location": "Kupwara Main",
            "district": "Kupwara",
            "pay": "₹800/day",
            "min_education": "12th",
            "max_age": 40,
            "deadline": "48h",
            "Action Needed": "Local residence certificate required"
        },
        {
            "title": "Assistant Professor (Physics)",
            "location": "Srinagar",
            "district": "Srinagar",
            "pay": "₹50,000/month",
            "min_education": "Post-Graduate",
            "max_age": 40,
            "deadline": "1 week"
        }
    ]
    
    profile_path = os.path.expanduser("~/.openclaw/user/profile.yaml")
    engine = LOR_Engine(profile_path)
    print(engine.generate_daily_report(mock_db))

if __name__ == "__main__":
    main()
