import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("OPEN_AI_API_KEY")
print(api_key)
client = OpenAI(api_key=api_key)


response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a song about Jack Sparrow."},
    ],
)

print(response.choices[0].message.content)
