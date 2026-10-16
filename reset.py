def reset():
    import os
    import shutil
    path = 'results'
    models = [str(x) + '-bit' for x in range(2,7)]
    datasets = ['MMLU-PRO','ARC-CHALLENGE','HUMANEVAL+','MATH-500']
    print(models)
    #delete folder
    for x in os.listdir(path):
        shutil.rmtree(f'{path}/{x}')
    #reconstruct folder
    for dataset in datasets:
        for model in models:
            os.makedirs(f'{path}/{dataset}/{model}',exist_ok=True)