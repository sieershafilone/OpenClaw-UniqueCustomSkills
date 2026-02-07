---
name: spotify-surface
description: Spotify integration for discovery and synchronized playback across Chat and WebUI.
---

# Spotify Unified Audio Surface

Unified interface for Spotify track discovery, metadata management, and synchronized playback delivery.

## 🚀 Features

- **TOS Compliant**: Never downloads or proxies full Spotify audio.
- **Synchronized Outputs**: Delivers 30s previews to Chat and interactive players to WebUI.
- **Metadata Ledger**: Maintains a persistent record of all resolved tracks in `media/spotify/`.
- **Cross-Platform**: Works across Telegram, WhatsApp, and the OpenClaw WebUI.

## 🛠️ Commands

| Command | Action |
|---------|--------|
| `play <song>` | Search and play a song in WebUI + Chat |
| `send <song>` | Resolve and send a 30s preview to Chat |
| `song <name>` | Display track metadata and playback options |

## 🧩 Workspace Contract

Metadata is stored at `media/spotify/<track_id>.json`.

```json
{
  "id": "5Sg09MvHqNWPWsYeuY2toY",
  "type": "spotify_track",
  "title": "Blinding Lights",
  "artist": "The Weeknd",
  "album": "After Hours",
  "duration_ms": 200040,
  "spotify_url": "https://open.spotify.com/track/5Sg09MvHqNWPWsYeuY2toY",
  "embed_url": "https://open.spotify.com/embed/track/5Sg09MvHqNWPWsYeuY2toY",
  "preview_url": "https://p.scdn.co/mp3-preview/...",
  "requested_from": "telegram",
  "created_at": "2026-02-07T13:40:00Z"
}
```

## 🛡️ Constraints

- **No full downloads**.
- **No audio proxying**.
- **WebUI must use Spotify Embed**.
- **Chat previews are limited to 30s**.
