---
name: omnipublisher
description: Multi-platform content publisher for social media and messaging channels with compliance guards, scheduling, and platform-specific adaptation.
---

# OmniPublisher (Nuclear Edition) v1.1.0

Automated reel, short, long video, image, and text distribution for high-bandwidth operations.

## ⚖️ Terms of Service & Constraints (Non-Negotiable)

- **Shadow/Unofficial APIs**: Strictly forbidden. Uses official Bot APIs or Business APIs only.
- **Bypassing**: No bypassing of platform security or human-verification systems.
- **Robotic Scheduling**: Prohibited. All scheduling must use jitter/windowing to maintain human-like patterns.
- **Content**: No monolithic blasts. Content is mutated per platform to fit native culture.

## 🏗️ Architecture

- **Content Normalizer**: Adapts single input to platform-specific limits (X: 280 chars, Insta: hashtags, YT: title/desc).
- **Media Processor**: FFmpeg pipeline for aspect ratio (9:16 vs 16:9), duration trimming, and compression.
- **Platform Router**: Handles individual adapter lifecycle and failures.
- **Compliance Guard**: Anti-blast protection, content hashing, and rate-limit proximity detection.
- **Audit Logger**: Detailed success/failure history with replay support.

## 🛠️ Platform Rules

| Platform | Video Limit | Image | Text Limit |
|----------|-------------|-------|------------|
| **Twitter (X)** | ≤140s | ✔️ | ≤280 chars |
| **Instagram** | Reels (≤90s) | ✔️ | hashtags req |
| **YouTube** | Shorts (≤60s) | ✔️ | Title + Desc |
| **Facebook** | Standard | ✔️ | Links allowed |
| **Telegram** | Standard | ✔️ | MD/HTML |
| **WhatsApp** | Standard | ✔️ | Caption req |

## 🚀 Messaging Integration

### Telegram (Bot API)
- **Supported**: Text, Image, Video, Channel/Group posting.
- **Interface**: `sendText`, `sendPhoto`, `sendVideo`.
- **Note**: Uses `telegram_bot_token`.

### WhatsApp (Business API)
- **Supported**: Text, Image, Video, Captioned Media.
- **Interface**: `sendMessage`, `sendMedia`.
- **Note**: Requires approved provider. Template messages enforced for cold outreach.

## 🧩 Compliance Logic

- ❌ **No Bulk Cold Messaging**: Messaging is limited to opted-in targets.
- ❌ **No Identical Blast Timing**: Staggered windows are mandatory.
- ✅ **Per-Recipient Jitter**: Even in windows, each message has a unique offset.
- ✅ **Opt-in Ledger**: `if recipient.lastMessage < cooldown: skip(recipient)`.

## invocation Example

```json
{
  "skill": "omnipublisher",
  "content": { "type": "image", "path": "./launch.png" },
  "caption": "Launch is live.",
  "platforms": ["telegram", "whatsapp"],
  "targets": {
    "telegram": { "chats": ["@mychannel"] },
    "whatsapp": { "recipients": ["+91XXXXXXXXXX"] }
  },
  "schedule": {
    "mode": "window",
    "window": { "min_delay": 120, "max_delay": 900 }
  }
}
```
