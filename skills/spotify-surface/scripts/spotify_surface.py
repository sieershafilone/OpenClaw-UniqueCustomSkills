#!/usr/bin/env python3
import os
import sys
import json
import time
import requests
from pathlib import Path
from datetime import datetime, timezone

class SpotifySurface:
    def __init__(self, workspace_path: str):
        self.workspace = Path(workspace_path)
        self.media_dir = self.workspace / "media" / "spotify"
        self.media_dir.mkdir(parents=True, exist_ok=True)
        self.config_path = self.workspace / ".openclaw" / "openclaw.json"
        
        # Load credentials
        self.client_id = os.environ.get("SPOTIFY_CLIENT_ID")
        self.client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
        self.access_token = None

    def _get_access_token(self):
        """Official Client Credentials Flow."""
        if not self.client_id or not self.client_secret:
            return None
            
        url = "https://accounts.spotify.com/api/token"
        try:
            r = requests.post(url, data={"grant_type": "client_credentials"}, 
                             auth=(self.client_id, self.client_secret))
            if r.status_code == 200:
                self.access_token = r.json().get("access_token")
                return self.access_token
        except Exception as e:
            print(f"[ERR] Token fetch failed: {e}", file=sys.stderr)
        return None

    def search_track(self, query: str):
        """Search Spotify for the best track match."""
        if not self.access_token and not self._get_access_token():
            print("[WARN] No Spotify credentials found. Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET.")
            return None

        url = "https://api.spotify.com/v1/search"
        params = {"q": query, "type": "track", "limit": 1}
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        try:
            r = requests.get(url, params=params, headers=headers)
            if r.status_code == 200:
                tracks = r.json().get("tracks", {}).get("items", [])
                if tracks:
                    return tracks[0]
        except Exception as e:
            print(f"[ERR] Search failed: {e}", file=sys.stderr)
        return None

    def persist_metadata(self, track: dict, requested_from: str):
        """Store metadata JSON in workspace."""
        track_id = track["id"]
        metadata = {
            "id": track_id,
            "type": "spotify_track",
            "title": track["name"],
            "artist": track["artists"][0]["name"],
            "album": track["album"]["name"],
            "duration_ms": track["duration_ms"],
            "spotify_url": track["external_urls"]["spotify"],
            "embed_url": f"https://open.spotify.com/embed/track/{track_id}",
            "preview_url": track.get("preview_url"),
            "requested_from": requested_from,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        file_path = self.media_dir / f"{track_id}.json"
        with open(file_path, "w") as f:
            json.dump(metadata, f, indent=2)
            
        return metadata

    def emit_outputs(self, metadata: dict):
        """Emit synchronized outputs for Chat and WebUI."""
        # Output A: Chat
        chat_output = {}
        if metadata.get("preview_url"):
            chat_output = {
                "type": "chat.audio_preview",
                "file_url": metadata["preview_url"],
                "caption": f"🎵 {metadata['title']} – {metadata['artist']} ▶️ Playing in OpenClaw WebUI 🔗 Open in Spotify: {metadata['spotify_url']}"
            }
        else:
            chat_output = {
                "type": "chat.message",
                "text": f"🎵 {metadata['title']} – {metadata['artist']} ▶️ Playing in OpenClaw WebUI 🔗 Open in Spotify: {metadata['spotify_url']}"
            }
            
        # Output B: WebUI
        webui_output = {
            "type": "webui.media",
            "media_kind": "spotify",
            "track_id": metadata["id"],
            "title": metadata["title"],
            "artist": metadata["artist"],
            "embed_url": metadata["embed_url"],
            "controls": {
                "play": True,
                "pause": True,
                "next": True,
                "volume": True
            }
        }
        
        # Dual-output stream
        print(json.dumps({"outputs": [chat_output, webui_output]}))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: spotify_surface.py <source> <query>")
        sys.exit(1)
        
    source = sys.argv[1] # e.g., telegram, whatsapp
    query = " ".join(sys.argv[2:])
    
    surface = SpotifySurface("/home/ky11rie/.openclaw/workspace")
    track = surface.search_track(query)
    
    if track:
        metadata = surface.persist_metadata(track, source)
        surface.emit_outputs(metadata)
    else:
        print(json.dumps({"outputs": [{"type": "chat.message", "text": f"No Spotify match found for: {query}"}]}))
