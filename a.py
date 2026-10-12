from ollama import chat

response = chat(
    model='qwen3.5:4b',
    messages=[
        {
            'role': 'user',
            'content': 'What is 5+5? Explain too',
        },
    ],
)

# Access the text response directly
print(response.message.content)
total_duration_sec = response.total_duration / 1e9  # Convert nanoseconds to seconds
prompt_eval_sec = response.prompt_eval_duration / 1e9
eval_sec = response.eval_duration / 1e9
print(f"Total duration: {total_duration_sec:.2f} seconds")
print(f"Prompt evaluation duration: {prompt_eval_sec:.2f} seconds")
print(f"Evaluation duration: {eval_sec:.2f} seconds")   