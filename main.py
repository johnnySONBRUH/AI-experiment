def main():
    from datasets import load_dataset
    #MMLU-Pro
    dataset = load_dataset("TIGER-Lab/MMLU-Pro")
    print(dataset,'MMLU-Pro')
    dataset.save_to_disk(dataset, 'MMLU-Pro')
    #ARC-Challenge
    dataset = load_dataset("allenai/ai2_arc", "ARC-Challenge")
    print(dataset,'ARC-Challenge')
    dataset.save_to_disk(dataset, 'ARC-Challenge')
    #HumanEval+
    dataset = load_dataset("evalplus/humanevalplus")
    print(dataset,'HumanEval+')
    dataset.save_to_disk(dataset, 'HumanEval+')
    #MATH-500
    dataset = load_dataset("HuggingFaceH4/MATH-500")
    print(dataset,'MATH-500')
    dataset.save_to_disk(dataset, 'MATH-500')
if __name__ == '__main__':
    main()