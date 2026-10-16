def summariseJSON(dataset,model):
    import json
    import os
    path = 'results'
    result = {}
    with open(f'{path}/{dataset}/{model}/data.json','r') as f:
        d = json.loads(f.read())
        return [d,d.keys()]
def compile():
    import os
    path = 'results'
    models = [str(x) + '-bit' for x in range(2,7)]
    datasets = ['MMLU-PRO','ARC-CHALLENGE','HUMANEVAL+','MATH-500']
    result = {}
    for dataset in datasets:
        d = {}
        for model in models:
            d2 = {}
            p = f'{path}/{dataset}/{model}'
            data,keys = summariseJSON(dataset,model)
            d2['time_to_first_token'] = data['time_to_first_token']
            d2['tokens_per_second'] = data['tokens_per_second']
            d2['total_duration'] = data['total_duration']
            for gpu in data['gpu']:
                print(gpu)
            d[model] = d2