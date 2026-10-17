def main():
    from datasets import load_from_disk
    #MMLU-Pro
    dataset = load_from_disk('datasets/MMLU-Pro')['test']
    print(dataset['question'][0],'MMLU-Pro')
    print(dataset['options'][0],'MMLU-Pro')
    print(dataset['answer_index'][0],'MMLU-Pro')
    #ARC-Challenge
    dataset = load_from_disk('datasets/ARC-Challenge')['test']
    print(dataset['question'][0],'ARC-Challenge')
    print(dataset['choices'][0],'ARC-Challenge')
    print(dataset['answerKey'][0],'ARC-Challenge')
    #HumanEval+
    dataset = load_from_disk('datasets/HumanEval+')['test']
    print(dataset['prompt'][0],'HumanEval+')
    print(dataset['canonical_solution'][0],'HumanEval+')
    #MATH-500
    dataset = load_from_disk('datasets/MATH-500')['test']
    print(dataset['problem'][0],'MATH-500')
    print(dataset['answer'][0],'MATH-500')
if __name__ == '__main__':
    main()