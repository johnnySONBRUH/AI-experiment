def reset():
    import os
    import shutil
    path = 'results'
    models = [str(x) + '-bit' for x in range(2,7)]
    print(models)
    #delete folder
    for x in os.listdir(path):
        shutil.rmtree(f'{path}/{x}')
    #reconstruct folder
    