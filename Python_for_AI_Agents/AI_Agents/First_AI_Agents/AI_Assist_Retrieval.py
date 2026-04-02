import json
import os
from openai import OpenAI
from pydantic import BaseModel, Field

client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))


def search_kb(question: str):
    with open("kb-for-retrieval.json", "r") as f:
        return json.load(f)


tools = [
    {
        "type": "function",
        "function": {
            "name": "search_kb",
            "description": "Get the answer to the user's question from the knowledge base.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                },
                "required": ["question"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]

system_prompt = (
    "You are a helpful assistant that answers questions based on the knowledge base"
)

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What is the return policy of the store?"},
]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)


completion.model_dump()


def call_function(name, args):
    if name == "search_kb":
        return search_kb(**args)


for tool_call in completion.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    messages.append(completion.choices[0].message)

    result = call_function(name, args)
    messages.append(
        {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)}
    )


class KBResponse(BaseModel):
    answer: str = Field(
        description="The answer to the user's question based on the knowledge base"
    )
    source: int = Field(
        description="The id of the document in the knowledge base that contains the answer"
    )


completion_2 = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    response_format=KBResponse,
)

final_response = completion_2.choices[0].message.parsed
print(final_response.answer)
print(final_response.source)
