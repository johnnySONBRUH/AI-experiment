def writeData(data,dataset,model):
    import json
    d = {
        'MMLU-PRO':"results/MMLU-PRO/",
        'ARC-CHALLENGE':"results/ARC-CHALLENGE/",
        'HUMANEVAL+':"results/HUMANEVAL+/",
        'MATH-500':"results/MATH-500/"
    }
    modelDict = {
        'hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q2_K':'2-bit',
        'hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q3_K_M':'3-bit',
        'hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q4_K_M':'4-bit',
        'hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q5_K_M':'5-bit',
        'hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q6_K':'6-bit'
    }
    path = d[dataset] + f'{modelDict[model]}/'
    jsonPath = path + 'data.json'
    resultsPath = path + 'results.json'
    with open(jsonPath,'w') as f:
        f.write(json.dumps(data,indent=4))