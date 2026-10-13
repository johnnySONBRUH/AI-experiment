from ollama import chat
from collections import defaultdict
from checkAnswers import checkByName
import os
import psutil
import threading
import time
import nvsmi
from loadByName import loadByName
from data import writeData
for x in ['MMLU-PRO','ARC-CHALLENGE','HUMANEVAL+','MATH-500']:
    tests = loadByName(x)
    continueLoggingCPUAndRam = True
    resources = defaultdict(list)
    answers = {}
    def getCPUandRAM():
        while continueLoggingCPUAndRam:
            process_name = "llama-server.exe" 
            pids = [proc.pid for proc in psutil.process_iter() if proc.name().lower() == process_name.lower()]
            process = psutil.Process(pids[0]) if pids else None
            cpu_usage = process.cpu_percent(interval=1)
            ram_usage = process.memory_percent()
            ram_used = process.memory_info().rss / (1024 ** 2)
            disk_usage = psutil.disk_usage("/").percent
            for gpu in nvsmi.get_gpus():
                print(f"ID: {gpu.id} | Name: {gpu.name} | VRAM: {gpu.mem_total}, {gpu.mem_used} | Util: {gpu.gpu_util}%")
            resources['gpu'].append({gpu.id: {'name': gpu.name, 'vram_total': gpu.mem_total, 'vram_used': gpu.mem_used, 'utilization': gpu.gpu_util}})
            resources['cpu'].append(cpu_usage)
            resources['ram'].append({'usage_percent': round(ram_used,2), 'used_mb': ram_used})
            resources['disk'].append(disk_usage)
            print(f"CPU Usage: {cpu_usage}%")
            print(f"RAM Usage: {ram_usage}%")
            print(f"RAM Used: {ram_used:.2f} MB")
            print(f"Disk Usage: {disk_usage}%")
            time.sleep(1)
    timeToFirstToken = None # seconds
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
    cpu_and_ram_thread = threading.Thread(target=getCPUandRAM, daemon=True)
    cpu_and_ram_thread.start()
    fullResponse = ''
    for chunk in stream:
        if timeToFirstToken is None:
            timeToFirstToken = time.perf_counter() - start_time
        fullResponse += chunk['message']['content']
        print(chunk['message']['content'],end='',flush=True)
        final_response = chunk
    tps = (final_response.eval_count / final_response.eval_duration) * 1e9 #tokens per second
    answers['response'] = fullResponse
    totalDuration = final_response.total_duration / 1e9 #seconds
    resources['time_to_first_token'] = timeToFirstToken
    resources['tokens_per_second'] = tps
    resources['total_duration'] = totalDuration
    print('\n')
    print('Time to first token:', timeToFirstToken,'(seconds)')
    print('Tokens per second (eval):', tps,'(Tokens per second)')   
    print('Total duration: ',totalDuration,'(seconds)')
    continueLoggingCPUAndRam = False
    cpu_and_ram_thread.join()
    writeData(resources, 'MMLU-PRO')
    checkByName(x,answers)