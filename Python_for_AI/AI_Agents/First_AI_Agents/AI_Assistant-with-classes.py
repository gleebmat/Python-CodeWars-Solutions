import os
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "Extract the event information from the following text",
        },
        {
            "role": "user",
            "content": "We are going to have a meeting with Alice and Bob on the 17th of April, 2026",
        },
    ],
    response_format=CalendarEvent,
)

event = completion.choices[0].message.parsed
print(event.name)
print(event.date)
print(event.participants)
