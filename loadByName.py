def loadByName(name):
    from datasets import load_from_disk
    from collections import defaultdict
    def extract_ground_truth(dataset_answer_string):
        if "####" in dataset_answer_string:
            ans = dataset_answer_string.split("####")[1].strip()
            return ans.replace(",", "")
        return ""
    d = {
        'PIQA':"PIQA",
        'ARC-CHALLENGE':"ARC-Challenge",
        'GSM8K':"GSM8K"
    }
    dataset = load_from_disk(f'datasets/{d[name]}')['test']
    returnDict = defaultdict(list)
    prompt = ''
    if name == 'PIQA':
        prompt = 'Provide the answer which is the index of the correct option.\n'
        for x in range(len(dataset)):
            returnDict['questions'].append(dataset['goal'][x])
            returnDict['options'].append([dataset['sol1'][x],dataset['sol2'][x]])
            returnDict['answers'].append(dataset['label'][x])
    elif name == 'ARC-CHALLENGE':
        prompt = 'Provide only the alphabet of the correct option as your answer. \n'
        for x in range(len(dataset)):
            returnDict['questions'].append(dataset['question'][x])
            returnDict['answers'].append(dataset['answerKey'][x])
            opts = []
            for y in range(len(dataset['choices'][x]['text'])):
                opts.append(f'{dataset['choices'][x]['label'][y]}. {dataset['choices'][x]['text'][y]}')
            returnDict['options'].append('\n'.join(opts))
    elif name == "GSM8K":
        prompt = 'Solve this Mathmatics problem.\n'
        for x in range(len(dataset)):
            returnDict['questions'].append(dataset['question'][x])
            returnDict['options'].append(None)
            returnDict['answers'].append(extract_ground_truth(dataset['answer'][x]))
    prompt += 'Strictly format your response like this: ANSWER: {answer} STOP' + '\n'
    returnDict['prompt'] = [prompt]
    return returnDict