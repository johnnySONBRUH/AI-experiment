DATASET_CONFIG = {
    'MMLU-PRO':{
        'ctx':8192,
        'predict':2048
    },
    'ARC-CHALLENGE':{
        'ctx':4096,
        'predict':1024
    },
    'HUMANEVAL+':{
        'ctx':16384,
        'predict':2048
    },
    'MATH-500':{
        'ctx':16384,
        'predict':4096
    }
}
DATASETS = ['MMLU-PRO','ARC-CHALLENGE','HUMANEVAL+','MATH-500']
MODELS = ['hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q2_K','hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q3_K_M','hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q4_K_M','hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q5_K_M','hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q6_K']
MODELS_BIT = [str(x) + '-bit' for x in range(2,7)]