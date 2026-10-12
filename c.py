import psutil

process_name = "llama-server.exe"  # or "chrome.exe" on Windows

# Find all matching process IDs
pids = [proc.pid for proc in psutil.process_iter() if proc.name().lower() == process_name.lower()]

print(f"PIDs for {process_name}: {pids}")
