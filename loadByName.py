def loadByName(name):
    from datasets import load_from_disk
    from collections import defaultdict
    d = {
        'MMLU-PRO':"MMLU-Pro",
        'ARC-CHALLENGE':"ARC-Challenge",
        'HUMANEVAL+':"HumanEval+",
        'MATH-500':"MATH-500"
    }
    dataset = load_from_disk(d[name])['test']
    returnDict = defaultdict(list)
    prompt = ''
    if name == 'MMLU-PRO':
        prompt = 'Solve these problems and provide the answer which is the index of the correct option.\n'
        for x in range(len(dataset)):
            returnDict['questions'].append(dataset['question'][x])
            returnDict['answers'].append(dataset['answer_index'][x])
            returnDict['options'].append(dataset['options'][x])
    elif name == 'ARC-CHALLENGE':
        prompt = 'Solve these problems and provide the answer which is the alphabet of the correct option. For example, the first option is A and the second is B and so on so forth. If the answer is not present in the options, provide the index of the option which is closest to the answer. If there are multiple options which are equally close to the answer, provide the index of the first one. If there are no options, provide -1 as the answer. Provide only the index of the correct option as your answer. \n'
        for x in range(len(dataset)):
            returnDict['questions'].append(dataset['question'][x])
            returnDict['answers'].append(dataset['answerKey'][x])
            returnDict['options'].append(dataset['choices'][x]['text'])
    elif name == "MATH-500":
        prompt = 'Solve these Mathmatics problems and state your answer in the end. \n'
        for x in range(len(dataset)):
            returnDict['questions'].append(dataset['problem'][x])
            returnDict['options'].append(None)
            returnDict['answers'].append(dataset['answer'][x])
    elif name == 'HUMANEVAL+':
        prompt = 'Solve these programming problems and provide the code in the end. \n'
        for x in range(len(dataset)):
            returnDict['questions'].append(dataset['prompt'][x])
            returnDict['options'].append(None)
            returnDict['answers'].append(dataset['canonical_solution'][x])
    prompt += 'Do not explain yourself. Just return the answer.'
    returnDict['prompt'] = [prompt]
    return returnDict