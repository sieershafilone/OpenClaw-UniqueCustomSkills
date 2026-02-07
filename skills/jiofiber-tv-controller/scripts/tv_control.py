import sys
import os
from ppadb.client import Client as AdbClient

# ADB Keycodes
KEY_POWER = 26
KEY_PLAY_PAUSE = 85
KEY_UP = 19
KEY_DOWN = 20
KEY_LEFT = 21
KEY_RIGHT = 22
KEY_ENTER = 66
KEY_BACK = 4
KEY_HOME = 3
KEY_VOLUP = 24
KEY_VOLDOWN = 25
KEY_MUTE = 164

def get_device(ip):
    client = AdbClient(host="127.0.0.1", port=5037)
    # Note: ppadb expects an adb server to be running.
    # If no adb server is running, this will fail.
    # However, OpenClaw nodes often have adb server available.
    try:
        client.remote_connect(ip, 5555)
        device = client.device(f"{ip}:5555")
        return device
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def control_tv(ip, action, params=None):
    device = get_device(ip)
    if not device:
        return f"Error: Could not connect to {ip}"
    
    if action == "power":
        device.shell(f"input keyevent {KEY_POWER}")
        return "Toggled Power"
    elif action == "play":
        device.shell(f"input keyevent {KEY_PLAY_PAUSE}")
        return "Toggled Play/Pause"
    elif action in ["up", "down", "left", "right", "enter", "back", "home"]:
        key = {
            "up": KEY_UP, "down": KEY_DOWN, "left": KEY_LEFT, 
            "right": KEY_RIGHT, "enter": KEY_ENTER, "back": KEY_BACK, "home": KEY_HOME
        }[action]
        device.shell(f"input keyevent {key}")
        return f"Sent {action}"
    elif action == "yt":
        # Launch YouTube search or specific video
        query = params if params else ""
        # Generic YT Search Intent
        device.shell(f"am start -a android.intent.action.VIEW \"https://www.youtube.com/results?search_query={query}\"")
        return f"Searching YouTube for: {query}"
    elif action == "vol":
        level = params.lower() if params else "up"
        key = KEY_VOLUP if level == "up" else KEY_VOLDOWN if level == "down" else KEY_MUTE
        device.shell(f"input keyevent {key}")
        return f"Volume {level}"
    else:
        return f"Unknown action: {action}"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python tv_control.py <ip> <action> [params]")
        sys.exit(1)
    
    ip = sys.argv[1]
    action = sys.argv[2]
    params = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else None
    print(control_tv(ip, action, params))
