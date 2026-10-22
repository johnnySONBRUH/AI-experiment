def main():
    from datasets import load_from_disk
    #PIQA
    dataset = load_from_disk('datasets/PIQA')['validation']
    print(dataset['goal'][1],'PIQA')
    print(dataset['sol1'][1],'PIQA')
    print(dataset['sol2'][1],'PIQA')
    print(dataset['label'][1],'PIQA')
    #ARC-Challenge
    dataset = load_from_disk('datasets/ARC-Challenge')['test']
    print(dataset['question'][0],'ARC-Challenge')
    print(dataset['choices'][0],'ARC-Challenge')
    print(dataset['answerKey'][0],'ARC-Challenge')
    #GSM8K
    dataset = load_from_disk('datasets/GSM8K')['test']
    print(dataset)
    print(dataset['question'][0],'GSM8K')
    print(dataset['answer'][0],'GSM8K')
if __name__ == '__main__':
    main()