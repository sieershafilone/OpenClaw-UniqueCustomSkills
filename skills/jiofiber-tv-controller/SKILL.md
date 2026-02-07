---
name: jiofiber-tv-controller
description: Control YouTube playback and navigation on JioFiber TV via ADB remote-control emulation.
---

# JioFiberTVController

Role: Accept text commands from Telegram/WhatsApp and control YouTube playback on JioFiber TV.

## Prerequisites

1.  **Enable Developer Options** on your JioFiber TV.
2.  **Enable Network Debugging** (ADB over Network).
3.  Ensure the TV and this OpenClaw instance are on the same network or accessible via IP.

## Commands

| Command | Action |
|---------|--------|
| `tv.connect <ip>` | Connect to the TV IP address |
| `tv.power` | Toggle power (ON/OFF) |
| `tv.play` / `tv.pause` | Toggle YouTube playback |
| `tv.yt <query>` | Search and play on YouTube |
| `tv.vol up/down/mute` | Control volume |
| `tv.up/down/left/right` | Directional navigation |
| `tv.enter` | Select/Enter |
| `tv.back` | Go back |
| `tv.home` | Go to Home screen |

## Implementation

Uses `adb` (Android Debug Bridge) over network to send keyevents and intents to the JioFiber STB.
