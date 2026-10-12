from ollama import chat
import time
timeToFirstToken = None
start_time = time.time()
stream = chat(
    model='qwen3.5:4b',
    messages=[
        {
            'role': 'user',
            'content': 'What is 5+5? Explain too',
        },
    ],
    stream=True
)
final_response = ''
for chunk in stream:
    if timeToFirstToken is None:
        timeToFirstToken = time.perf_counter() - start_time
    print(chunk['message']['content'],end='',flush=True)
    final_response = chunk
tps = final_response.eval_count / (final_response.eval_duration * 1000000000)
print('Time to first token:', timeToFirstToken)
print('Tokens per second (eval):', tps)
print('Total duration: ',final_response.total_duration)