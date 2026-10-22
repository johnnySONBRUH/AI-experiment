import constants
import time
from ollama import chat
from collections import defaultdict
from checkAnswers import checkByName
import os
import re
import psutil
import threading
import time
import nvsmi
from loadByName import loadByName
from reset import reset
from compileResults import compile
from data import writeData
reset()
try:
    chat(model=model,messages=[],keep_alive=0)
except Exception:
    pass
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
        print(f'Evaluating {model} on {dataset}')
        for index in range(len(tests['questions'][:5])):
            print(index,'Current')
            timeToFirstToken = None # seconds
            start_time = time.perf_counter()
            continueLoggingCPUAndRam = True
            fullResponse = ''
            final_response = ''
            prompt = f'{tests["prompt"][0] + tests['questions'][index] + ('\nOptions: ' + (str(tests['options'][index]) if tests['options'][index] is not None else 'No options'))} \nAnswer Concisely'
            print("Current prompt: \n" + prompt)
            stream = chat(
                model=model,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                    },
                ],
                options = {
                    'temperature': 0.0,  
                    'seed': 42,        
                    'num_ctx': 8192,      
                    'num_predict': 2048   
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
            if dataset != 'GSM8K':
                answers['response'].append(fullResponse[8:len(fullResponse) - 5])
            else:
                n = re.search(r'\d+',fullResponse[8:len(fullResponse) - 5]).group()
                answers['response'].append(n)
            answers['answers'].append(tests['answers'][index])
            print("Stop reason: " + final_response.done_reason)
            print('Full response: ' + fullResponse)
            tps = (final_response.eval_count / (final_response.eval_duration / 1e9)) if final_response.eval_duration > 0 else 0
            resources['time_to_first_token'].append(timeToFirstToken)
            resources['tokens_per_second'].append(tps)
            resources['total_duration'].append(final_response.total_duration / 1e9)
        print(f'Evaluating {model} on {dataset} done.')
        print(answers)
        continueLoggingCPUAndRam = False
        cpu_and_ram_thread.join()
        writeData(resources, dataset, model)
        print(checkByName(answers,dataset,model),'answers')
        time.sleep(5)
    try:
        chat(model=model,messages=[],keep_alive=0)
    except Exception:
        pass
    time.sleep(10)
compile()