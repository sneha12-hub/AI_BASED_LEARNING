import openai

openai.api_key = "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"

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello, how are you?"}]
)

print(response["choices"][0]["message"]["content"])
