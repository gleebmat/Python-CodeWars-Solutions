import json
import os
import requests
from openai import OpenAI
from pydantic import BaseModel, Field

client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

user_input = input("Enter a location to get the current weather: ")


def get_weather(latitude: float, longitude: float):
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    )
    data = response.json()
    return data["current_weather"]


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "The latitude of the location",
                    },
                    "longitude": {
                        "type": "number",
                        "description": "The longitude of the location",
                    },
                },
                "required": ["latitude", "longitude"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]

system_prompt = "You are a helpful weather assistant."
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_input},
]


completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)


completion.model_dump()


def call_function(name, args):
    if name == "get_weather":
        return get_weather(**args)


for tool_call in completion.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    messages.append(completion.choices[0].message)

    result = call_function(name, args)
    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result),
        }
    )


class WeatherResponse(BaseModel):
    temperature: float = Field(description="The current temperature in Celsius")
    response: str = Field(
        description="A human-readable response describing the current weather"
    )


completion_2 = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    response_format=WeatherResponse,
)

final_response = completion_2.choices[0].message.parsed
print(final_response.temperature)
print(final_response.response)
