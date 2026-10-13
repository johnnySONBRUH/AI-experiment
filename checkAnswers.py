def checkByName(name,results):
    from datasets import load_from_disk
    from collections import defaultdict
    d = {
        'MMLU-PRO':"MMLU-Pro",
        'ARC-CHALLENGE':"ARC-Challenge",
        'HUMANEVAL+':"HumanEval+",
        'MATH-500':"MATH-500"
    }
    if name == "MMLU-PRO":
        correct = 0
        for x in range(len(results)):
            if results['answers'][x] == results['response'][x]:
                correct += 1