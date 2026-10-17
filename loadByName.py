def loadByName(name):
    from datasets import load_from_disk
    from collections import defaultdict
    d = {
        'MMLU-PRO':"MMLU-Pro",
        'ARC-CHALLENGE':"ARC-Challenge",
        'HUMANEVAL+':"HumanEval+",
        'MATH-500':"MATH-500"
    }
    dataset = load_from_disk(f'datasets/{d[name]}')['test']
    returnDict = defaultdict(list)
    prompt = ''
    if name == 'MMLU-PRO':
        prompt = 'Solve these problems and provide the answer which is the index of the correct option.\n'
        for x in range(len(dataset)):
            returnDict['questions'].append(dataset['question'][x])
            returnDict['answers'].append(dataset['answer_index'][x])
            returnDict['options'].append(dataset['options'][x])
    elif name == 'ARC-CHALLENGE':
        prompt = 'Solve these problems and provide only the alphabet of the correct option as your answer. \n'
        for x in range(len(dataset)):
            returnDict['questions'].append(dataset['question'][x])
            returnDict['answers'].append(dataset['answerKey'][x])
            opts = []
            for y in range(len(dataset['choices'][x]['text'])):
                opts.append(f'{dataset['choices'][x]['label'][y]}. {dataset['choices'][x]['text'][y]}')
            returnDict['options'].append('\n'.join(opts))
    elif name == "MATH-500":
        prompt = 'Solve these Mathmatics problems and state your answer in the end. \n'
        for x in range(len(dataset)):
            returnDict['questions'].append(dataset['problem'][x])
            returnDict['options'].append(None)
            returnDict['answers'].append(dataset['answer'][x])
    elif name == 'HUMANEVAL+':
        prompt = 'Solve these programming problems and provide the answer code in the end. \n'
        for x in range(len(dataset)):
            returnDict['questions'].append(dataset['prompt'][x])
            returnDict['options'].append(None)
            returnDict['answers'].append(dataset['canonical_solution'][x])
    prompt += 'Do not return an empty response and please format your response like this: ANSWER: {answer} STOP' + '\n'
    returnDict['prompt'] = [prompt]
    return returnDict