# OpenClaw Custom Skills

This repository contains custom skills and agents for the OpenClaw ecosystem, designed for autonomy, identity proxing, and specialized intelligence.

## Skills

### 🎭 Agent Doppelgänger (ADG)
**Location:** `skills/agent-doppelganger`
A policy-bounded identity proxy for real-world communication. It acts as a constrained autonomous delegate that communicates on your behalf (WhatsApp, Discord, etc.) while enforcing strict authority policies and matching your personal style.

### 🏔️ Local Opportunity Radar (Kashmir)
**Location:** `skills/local-opportunity-radar-kashmir`
A high-precision opportunity intelligence engine for Jammu & Kashmir. It aggregates local signals (DC office PDFs, WhatsApp groups, official notices) and filters them against a specific user eligibility profile to surface high-relevance income opportunities.

### 🐙 GitHub
**Location:** `skills/github`
Integration with the GitHub CLI (`gh`) to manage issues, pull requests, and CI runs directly from OpenClaw.

## Usage

These skills are designed to be loaded into an OpenClaw workspace.

1. Clone this repository into your OpenClaw workspace or skills directory.
2. Run `openclaw skill list` to verify availability.
3. Configure necessary secrets (e.g., in `~/.openclaw/openclaw.json` or environment variables).

## License

Private / Proprietary.
