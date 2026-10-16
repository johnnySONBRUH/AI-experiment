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
for model in ['hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q2_K','hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q3_K_M','hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q4_K_M','hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q5_K_M','hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q6_K']:
    for dataset in ['MMLU-PRO','ARC-CHALLENGE','HUMANEVAL+','MATH-500']:
        print(f'Current model: ({model}), Current dataset: ({dataset})')
        tests = loadByName(dataset)
        print(f'{dataset} loaded')
        resources = defaultdict(list)
        answers = defaultdict(list)
        def getCPUandRAM():
            while continueLoggingCPUAndRam:
                process_name = "ollama.exe" 
                pids = [proc.pid for proc in psutil.process_iter() if proc.name().lower() == process_name.lower()]
                process = psutil.Process(pids[0]) if pids else None
                cpu_usage = process.cpu_percent(interval=1)
                ram_usage = process.memory_percent()
                ram_used = process.memory_info().rss / (1024 ** 2)
                disk_usage = process.io_counters()
                read_mb = disk_usage.read_bytes / (1024 ** 2)
                write_mb = disk_usage.write_bytes / (1024 ** 2)
                disk_usage = {'read_mb': read_mb, 'write_mb': write_mb}
                for gpu in nvsmi.get_gpus():
                    resources['gpu'].append({gpu.id: {'name': gpu.name, 'vram_total': gpu.mem_total, 'vram_used': gpu.mem_used, 'utilization': gpu.gpu_util}})
                resources['cpu'].append(cpu_usage)
                resources['ram'].append({'usage_percent': round(ram_used,2), 'used_mb': ram_used})
                resources['disk'].append(disk_usage)
                time.sleep(1)
        timeToFirstToken = None # seconds
        start_time = time.perf_counter()
        totalEvalCount = 0
        totalEvalDuration = 0
        totalDuration = 0 #seconds
        #turn into a while loop that retries on done_reason=length
        print(f'Evaluating {model} on {dataset}')
        for index in range(len(tests['questions'])):
            print(index,'Current')
            continueLoggingCPUAndRam = True
            fullResponse = ''
            final_response = ''
            stream = chat(
                model=model,
                messages=[
                    {
                        'role': 'user',
                        'content': tests['prompt'][0] + tests['questions'][index],
                    },
                ],
                options = {
                    'num_ctx':8192, #16k tokens
                    'num_predict':4096
                },
                stream=True
            )
            cpu_and_ram_thread = threading.Thread(target=getCPUandRAM, daemon=True)
            cpu_and_ram_thread.start()
            for chunk in stream:
                if timeToFirstToken is None:
                    timeToFirstToken = time.perf_counter() - start_time
                fullResponse += chunk['message']['content']
                final_response = chunk
                print(chunk['message']['content'],end='',flush=True)
            print('\n')
            answers['response'].append(fullResponse)
            answers['answers'].append(tests['answers'][index])
            print("Stop reason: " + final_response.done_reason)
            print('Full response: ' + fullResponse)
            totalDuration += final_response.total_duration / 1e9 #seconds
            totalEvalCount += final_response.eval_count
            totalEvalDuration += final_response.eval_duration / 1e9 #seconds
        print(f'Evaluating {model} on {dataset} done.')
        print(answers)
        tps = (totalEvalCount / totalEvalDuration) * 1e9 if totalEvalDuration > 0 else 0 #tokens per second
        resources['time_to_first_token'] = timeToFirstToken
        resources['tokens_per_second'] = tps
        resources['total_duration'] = totalDuration
        continueLoggingCPUAndRam = False
        cpu_and_ram_thread.join()
        writeData(resources, dataset, model)
        print(checkByName(answers,dataset,model),'answers')