DATASETS = ['MMLU-PRO','ARC-CHALLENGE','HUMANEVAL+','MATH-500']
MODELS = ['hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q2_K','hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q3_K_M','hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q4_K_M','hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q5_K_M','hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q6_K']
MODELS_BIT = [str(x) + '-bit' for x in range(2,7)]