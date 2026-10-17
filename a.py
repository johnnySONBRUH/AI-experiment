import constants
from ollama import chat
from collections import defaultdict
from checkAnswers import checkByName
import os
import psutil
import threading
import time
import nvsmi
from loadByName import loadByName
from reset import reset
from compileResults import compile
from data import writeData
reset()
for model in constants.MODELS:
    for dataset in constants.DATASETS:
        def getCPUandRAM():
            last_read_bytes = None
            last_write_bytes = None
            while continueLoggingCPUAndRam:
                process_name = "ollama.exe" 
                pids = [proc.pid for proc in psutil.process_iter() if proc.name().lower() == process_name.lower()]
                process = psutil.Process(pids[0]) if pids else None
                if process:
                    cpu_usage = process.cpu_percent(interval=None)
                    ram_usage = process.memory_percent()
                    ram_used = process.memory_info().rss / (1024 ** 2)
                    disk_usage = process.io_counters()
                    if last_read_bytes is None:
                        last_read_bytes = disk_usage.read_bytes
                        last_write_bytes = disk_usage.write_bytes
                        read_mb = 0.0
                        write_mb = 0.0
                    else:
                        read_delta = disk_usage.read_bytes - last_read_bytes
                        write_delta = disk_usage.write_bytes - last_write_bytes
                        
                        last_read_bytes = disk_usage.read_bytes
                        last_write_bytes = disk_usage.write_bytes
                        
                        read_mb = read_delta / (1024 ** 2)
                        write_mb = write_delta / (1024 ** 2)
                    disk_usage_dict = {'read_mb': round(read_mb, 2), 'write_mb': round(write_mb, 2)}
                    for gpu in nvsmi.get_gpus():
                        resources['gpu'].append({
                            gpu.id: {
                                'name': gpu.name, 
                                'vram_total': gpu.mem_total, 
                                'vram_used': gpu.mem_used, 
                                'utilization': gpu.gpu_util
                            }
                        })
                    resources['cpu'].append(cpu_usage)
                    resources['ram'].append({'usage_percent': round(ram_usage, 2), 'used_mb': round(ram_used, 2)})
                    resources['disk'].append(disk_usage_dict)
                time.sleep(1)
        print(f'Current model: ({model}), Current dataset: ({dataset})')
        tests = loadByName(dataset)
        print(f'{dataset} loaded')
        resources = defaultdict(list)
        answers = defaultdict(list)
        timeToFirstToken = None # seconds
        start_time = time.perf_counter()
        totalEvalCount = 0
        totalEvalDuration = 0
        totalDuration = 0 #seconds
        print(f'Evaluating {model} on {dataset}')
        for index in range(len(tests['questions'][:3])):
            print(index,'Current')
            continueLoggingCPUAndRam = True
            fullResponse = ''
            final_response = ''
            prompt = f'Current prompt: {tests['prompt'][0] + tests['questions'][index] + ('\nOptions: ' + (str(tests['options'][index]) if tests['options'][index] != None else 'No options'))}'
            print(prompt)
            stream = chat(
                model=model,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                    },
                ],
                options = {
                    'num_ctx':16384, 
                    'num_predict':4096,
                    'temperature':0.0,
                    'stop':['STOP']
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
compile()