#!/usr/bin/env python3
"""
OmniPublisher (Nuclear Edition) v1.1.0
Core Orchestrator
"""

import sys
import os
import json
import time
import random
from pathlib import Path

# Add relative paths to sys.path for local imports
CURRENT_DIR = Path(__file__).parent.parent
sys.path.append(str(CURRENT_DIR))

from guards.compliance import ComplianceGuard
from normalizers.content import ContentNormalizer
from processors.media import MediaProcessor

class OmniPublisher:
    def __init__(self, workspace_path: str):
        self.workspace = Path(workspace_path)
        self.guard = ComplianceGuard(workspace_path)
        self.normalizer = ContentNormalizer()
        self.media = MediaProcessor()

    def publish(self, payload):
        print(f"[NUCLEAR] Initializing OmniPublisher v1.1.0 run...")
        
        content = payload.get("content", {})
        base_caption = content.get("caption", "")
        platforms = payload.get("platforms", [])
        targets = payload.get("targets", {})
        schedule = payload.get("schedule", {"mode": "now"})

        for platform in platforms:
            print(f"--- [Platform: {platform.upper()}] ---")
            
            # 1. Normalize Text
            processed_text = self.normalizer.normalize(base_caption, platform)
            
            # 2. Process Media
            if content.get("path"):
                final_media_path = self.media.process(content["path"], platform)
            else:
                final_media_path = None

            # 3. Compliance Check
            if not self.guard.check(platform, base_caption):
                continue

            # 4. Route to Adapter
            # In a live system, this calls adapters/twitter.py etc.
            self._execute_send(platform, processed_text, final_media_path, targets.get(platform))
            
            # 5. Log Success
            self.guard.log_post(platform, base_caption)

            # 6. Scheduling / Jitter
            if schedule.get("mode") == "window":
                win = schedule.get("window", {"min_delay": 5, "max_delay": 15})
                jitter = random.randint(win["min_delay"], win["max_delay"])
                print(f"[STEALTH] Waiting {jitter}s jitter before next platform...")
                time.sleep(jitter)

    def _execute_send(self, platform, text, media, target_group):
        """
        Nuclear Dispatcher.
        Connects to actual channel tools (message, bird, etc.)
        """
        print(f"[ADAPTER] Routing payload to {platform}...")
        if target_group:
            print(f"    [TARGETS] {target_group}")
        print(f"    [TEXT] {str(text)[:60]}...")
        if media:
            print(f"    [MEDIA] {media}")

if __name__ == "__main__":
    pub = OmniPublisher("/home/ky11rie/.openclaw/workspace")
    
    # Nuclear Demo Payload
    example = {
        "platforms": ["twitter", "telegram", "whatsapp"],
        "content": {
            "type": "image",
            "path": "launch.png",
            "caption": "The nuclear distribution system is now live across all sectors."
        },
        "targets": {
            "telegram": {"chats": ["@syer_updates"]},
            "whatsapp": {"recipients": ["+91XXXXXXXXXX"]}
        },
        "schedule": {
            "mode": "window",
            "window": {"min_delay": 1, "max_delay": 3}
        }
    }
    
    pub.publish(example)
