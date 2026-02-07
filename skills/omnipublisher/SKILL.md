---
name: omnipublisher
description: The ultimate cross-platform content distribution and messaging engine. Supports automated content mutation, scheduling, and anti-detection compliance guards.
---

# OmniPublisher (Nuclear Edition)

OmniPublisher is a heavy-duty multi-channel content orchestrator. It manages the lifecycle of a post or message from synthesis to multi-platform distribution, ensuring compliance, engagement optimization, and stealth.

## 🚀 Nuclear Features

- **Multi-Platform Distribution**: Twitter, Instagram, YouTube, Facebook, Telegram, and WhatsApp.
- **Content Mutation Engine**: Automatically rewrites captions and adjusts hashtags based on platform culture (e.g., professional for LinkedIn, minimal for X, emoji-dense for Insta).
- **Stealth Jitter & Windowing**: Beyond simple delays, uses probabilistic "windows" to simulate human activity and bypass bot detection.
- **Media Transcoding**: Auto-resizes and optimizes media (images/videos) to fit platform-specific aspect ratios and file size limits.
- **Drip & Sequential Logic**: Support for multi-step "drip" campaigns with recipient-level cooldown tracking.
- **Identity Proxying**: Seamlessly integrates with `agent-doppelganger` for personalized recipient interactions.
- **Engagement Loop**: Ingests platform feedback (likes, views, errors) back into workspace memory to improve future distribution strategies.

## 🛠️ Commands

| Command | Action |
|---------|--------|
| `publish.now <content>` | Instant blast to all default platforms |
| `publish.schedule <json>` | Advanced scheduled run with windowing |
| `publish.status <run_id>` | Check progress of a distribution job |
| `publish.cooldown <target>` | Check or reset cooldown for a specific recipient |

## 🛡️ Compliance Guards

- ❌ **Anti-Blast**: Prevents identical content hashes from being sent to the same recipient.
- ❌ **Bulk Protection**: Limits the number of targets per platform per hour.
- ✅ **Opt-in Ledger**: Tracks recipient opt-out status across all messaging channels.
- ✅ **Dynamic Jitter**: Injects 20-30% random noise into every scheduled timing.

## 🧩 Schema (Nuclear Payload)

```json
{
  "skill": "omnipublisher",
  "content": {
    "type": "video",
    "path": "./launch_clip.mp4",
    "optimize": true
  },
  "metadata": {
    "base_caption": "The new system is live.",
    "hashtags": ["tech", "ai", "future"]
  },
  "platforms": ["twitter", "telegram", "whatsapp"],
  "targets": {
    "telegram": { "chats": ["@my_channel"] },
    "whatsapp": { "recipients": ["+91XXXXXXXXXX"] }
  },
  "strategy": {
    "mode": "window",
    "window": { "min_delay": 300, "max_delay": 1200 },
    "mutate_content": true
  }
}
```

## 📂 Structure

- `adapters/`: Individual platform handlers (bot API, cloud API, CLI).
- `guards/`: Anti-spam, rate-limiting, and PII filters.
- `scripts/`: Content mutation and media optimization logic.
- `templates/`: Platform-specific caption templates.
