from ollama import chat
import os
import psutil
import threading
import time
import nvsmi
def getCPUandRAM():
    #pid = llama-server
    process_name = "llama-server.exe"  # or "chrome.exe" on Windows

# Find all matching process IDs
    pids = [proc.pid for proc in psutil.process_iter() if proc.name().lower() == process_name.lower()]

    process = psutil.Process(pids[0]) if pids else None
    while True:
        cpu_usage = process.cpu_percent(interval=1)
        ram_usage = process.memory_percent()
        ram_used = process.memory_info().rss / (1024 ** 2)  # Convert bytes to MB
        disk_usage = psutil.disk_usage("/").percent
        for gpu in nvsmi.get_gpus():
            print(f"ID: {gpu.id} | Name: {gpu.name} | VRAM: {gpu.mem_total}, {gpu.mem_used} | Util: {gpu.gpu_util}%")
        print(f"CPU Usage: {cpu_usage}%")
        print(f"RAM Usage: {ram_usage}%")
        print(f"RAM Used: {ram_used:.2f} MB")
        print(f"Disk Usage: {disk_usage}%")
        time.sleep(1)
timeToFirstToken = None
start_time = time.perf_counter()
stream = chat(
    model='qwen3.5:4b',
    messages=[
        {
            'role': 'user',
            'content': 'What is 5+5? Explain too',
        },
    ],
    stream=True
)
final_response = ''
cpu_and_ram_thread = threading.Thread(target=lambda: getCPUandRAM())
cpu_and_ram_thread.start()

for chunk in stream:
    if timeToFirstToken is None:
        timeToFirstToken = time.perf_counter() - start_time
    print(chunk['message']['content'],end='',flush=True)
    final_response = chunk
cpu_and_ram_thread.join()
tps = (final_response.eval_count / final_response.eval_duration) * 1e9
print('\n')
print('Time to first token:', timeToFirstToken,'(seconds)')
print('Tokens per second (eval):', tps,'(Tokens per second)')
print('Total duration: ',final_response.total_duration / 1e9,'(seconds)')