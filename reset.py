def reset():
    import os
    import shutil
    import constants
    path = 'results'
    models = constants.MODELS_BIT
    datasets = constants.DATASETS
    #delete folder
    for x in os.listdir(path):
        shutil.rmtree(f'{path}/{x}')
    #reconstruct folder
    for dataset in datasets:
        for model in models:
            os.makedirs(f'{path}/{dataset}/{model}',exist_ok=True)
if __name__ == '__main__':
    reset()