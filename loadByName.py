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
        prompt = 'Solve these problems and provide only the index of the correct option as your answer. \n'
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
    prompt += 'Format your response like this: ANSWER: {answer} STOP'
    returnDict['prompt'] = [prompt]
    return returnDict