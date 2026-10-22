from ollama import chat
stream = chat(
    model='hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q2_K',
    messages=[
        {
            'role':"user",
            'content':'What is 5 + 5? Explain why'
        },
    ],
    stream=True
)
f = ''
for c in stream:
    f += c['message']['content']
    print(c['message']['content'])
print(f)