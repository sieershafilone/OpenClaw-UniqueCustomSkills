import hashlib
import time
import json
from pathlib import Path

class ComplianceGuard:
    """
    Enforces platform safety, anti-spam, and rate-limit rules.
    """
    def __init__(self, workspace_path: str):
        self.history_dir = Path(workspace_path) / ".omnipublisher" / "history"
        self.history_dir.mkdir(parents=True, exist_ok=True)
        self.ledger_path = self.history_dir / "compliance_ledger.json"
        self.ledger = self._load_ledger()

    def _load_ledger(self):
        if self.ledger_path.exists():
            with open(self.ledger_path, 'r') as f:
                return json.load(f)
        return {"hashes": {}, "last_posts": {}}

    def _save_ledger(self):
        with open(self.ledger_path, 'w') as f:
            json.dump(self.ledger, f, indent=2)

    def check(self, platform, content_text, target=None) -> bool:
        """
        Hard stops for compliance.
        Returns True if safe to proceed.
        """
        content_hash = hashlib.sha256(content_text.encode()).hexdigest()
        
        # 1. Duplicate Check (Hash)
        target_key = f"{platform}:{target}" if target else platform
        if content_hash in self.ledger["hashes"].get(target_key, []):
            print(f"[GUARD] Blocked: Duplicate content hash for {target_key}")
            return False

        # 2. Burst Posting Check (Cooldown)
        last_post = self.ledger["last_posts"].get(target_key, 0)
        cooldown = 120 # 2 minutes minimum between same target
        if time.time() - last_post < cooldown:
            print(f"[GUARD] Blocked: Target {target_key} is in cooldown")
            return False

        return True

    def log_post(self, platform, content_text, target=None):
        content_hash = hashlib.sha256(content_text.encode()).hexdigest()
        target_key = f"{platform}:{target}" if target else platform
        
        if target_key not in self.ledger["hashes"]:
            self.ledger["hashes"][target_key] = []
        
        self.ledger["hashes"][target_key].append(content_hash)
        self.ledger["last_posts"][target_key] = time.time()
        self._save_ledger()
