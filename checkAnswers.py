def checkByName(results,dataset,model):
    from datasets import load_from_disk
    from collections import defaultdict
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
    path = d[dataset] + f'{modelDict[model]}/response.txt'
    name = dataset
    c = 0
    if name == "MMLU-PRO":
        for x in range(len(results['answers'])):
            if results['answers'][x] == results['response'][x]:
                c += 1
    elif name == 'ARC-CHALLENGE':
        for x in range(len(results['answers'])):
            if results['answers'][x] == results['response'][x]:
                c += 1
    elif name == 'MATH-500':
        for x in range(len(results['answers'])):
            if results['answers'][x] == results['response'][x]:
                c += 1
    elif name == 'HUMANEVAL+':
        for x in range(len(results['answers'])):
            if results['answers'][x] == results['response'][x]:
                c += 1
    with open(path,'w') as f:
        f.write(' '.join(results['response']) + '\n' + (str(results['answers'])) + str(c) + '<- correct')
    return c