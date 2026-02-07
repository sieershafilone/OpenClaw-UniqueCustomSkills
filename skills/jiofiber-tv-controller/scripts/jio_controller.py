import sys
import subprocess
import os

def handle_command(text):
    # Command format: tv.action params
    # Example: tv.yt Karan Aujla
    # Example: tv.connect 192.168.1.10
    
    parts = text.split()
    if not parts:
        return "No command provided."
    
    cmd = parts[0].lower()
    params = parts[1:] if len(parts) > 1 else []
    
    # Check if it's a TV command
    if not cmd.startswith("tv."):
        return "Not a TV command."
    
    action = cmd[3:]
    
    # Get IP from environment or config
    # In a real skill, we'd load this from manifest/config
    ip = os.environ.get("TV_IP", "192.168.1.10") # Default or placeholder
    
    if action == "connect" and params:
        ip = params[0]
        # In a real implementation, we'd save this IP to a state file
        return f"Targeting TV at {ip}..."
    
    script_path = os.path.join(os.path.dirname(__file__), "tv_control.py")
    result = subprocess.run(["python3", script_path, ip, action] + params, capture_output=True, text=True)
    return result.stdout.strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python jio_controller.py <command_text>")
        sys.exit(1)
    
    print(handle_command(sys.argv[1]))
