def summariseJSON(dataset,model):
    import json
    import os
    path = 'results'
    with open(f'{path}/{dataset}/{model}/data.json','r') as f:
        return json.loads(f.read())
def compile():
    import os
    import json
    import constants
    path = 'results'
    models = constants.MODELS_BIT
    datasets = constants.DATASETS
    result = {}
    for dataset in datasets:
        d = {}
        for model in models:
            d2 = {}
            p = f'{path}/{dataset}/{model}'
            data = summariseJSON(dataset,model)
            for gpu in data['gpu']:
                d2['gpuVRAM'] = gpu['vram_used'] + d2.get('gpuVRAM',0)
                d2['gpuUtilization'] = gpu['utilization'] + d2.get('gpuUtilization',0)
            for usage in data['cpu']:
                d2['cpu'] = usage + d2.get('cpu',0)
            for ram in data['ram']:
                d2['ramUsagePercent'] = ram['usage_percent'] + d2.get('ramUsagePercent',0)
                d2['ramUsedMB'] = ram['used_mb'] + d2.get('ramUsedMB',0)
            for disk in data['disk']:
                d2['diskRead'] = disk['read_mb'] + d2.get('diskRead',0)
                d2['diskWrite'] = disk['write_mb'] + d2.get('diskWrite',0)
            totalDisk = len(data['disk'])
            totalRam = len(data['ram'])
            totalCpu = len(data['cpu'])
            totalGpu = len(data['gpu'])
            d2['time_to_first_token'] = data['time_to_first_token']
            d2['tokens_per_second'] = data['tokens_per_second']
            d2['total_duration'] = data['total_duration']
            d2['gpuVram'] = round(d2['gpuVRAM'] / totalGPU, 3)
            d2['gpuUtilization'] = round(d2['gpuUtilization'] / totalGpu, 3)
            d2['cpu'] = round(d2['cpu'] / totalCpu, 3)
            d2['ramUsagePercent'] = round(d2['ramUsagePercent'] / totalRam, 3)
            d2['ramUsedMB'] = round(d2['ramUsedMB'] / totalRam, 3)
            d2['diskRead'] = round(d2['diskRead'] / totalDisk, 3)
            d2['diskWrite'] = round(d2['diskWrite'] / totalDisk, 3)
            d[model] = d2
        result[model] = d
    print(result)
    with open('overall.json','w') as f:
        f.write(json.dumps(result,indent=4))