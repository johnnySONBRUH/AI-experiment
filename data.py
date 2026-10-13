def writeData(data,dataset):
    import json
    d = {
        'MMLU-PRO':"results/MMLU-PRO/",
        'ARC-CHALLENGE':"results/ARC-CHALLENGE/",
        'HUMANEVAL+':"results/HUMANEVAL+/",
        'MATH-500':"results/MATH-500/"
    }
    path = d[dataset]
    jsonPath = path + 'data.json'
    resultsPath = path + 'results.json'
    with open(path,'w') as f:
        f.write(json.dumps(data,indent=4))