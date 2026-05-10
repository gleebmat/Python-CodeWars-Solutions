import time

import requests
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from dataclasses import dataclass
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.tools import create_retriever_tool
from langchain.agents import create_agent
from langchain.agents.middleware import (
    ModelRequest,
    ModelResponse,
    dynamic_prompt,
    wrap_model_call,
    AgentMiddleware,
    AgentState,
)
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, AIMessage, SystemMessage


# @dataclass
# class Context:
#     user_role: str


# basic_model = init_chat_model(model="gpt-4o-mini")
# advanced_model = init_chat_model(model="gpt-4.1-mini")


# @wrap_model_call
# def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
#     message_count = len(request.state["messages"])
#     if message_count > 3:
#         model = advanced_model
#     else:
#         model = basic_model
#     request.model = model
#     return handler(request)


# # @dynamic_prompt
# # def user_role_prompt(request: ModelRequest) -> str:

# #     base_prompt = "you are an assistant"
# #     user_role = request.runtime.context.user_role
# #     match user_role:
# #         case "expert":
# #             return f"{base_prompt} Provide detailed responses"
# #         case "beginner":
# #             return f"{base_prompt}keep explanations simple"
# #         case "child":
# #             return f"{base_prompt}Explain as if you are a five-year child"


# agent = create_agent(model=basic_model, middleware=[dynamic_model_selection])
# response = agent.invoke(
#     {"messages": [SystemMessage("Assistant"), HumanMessage("1+1=")]}
# )
# print(response["messages"][-1].content)
# print(response["messages"][-1].response_metadata["model_name"])


# agent = create_agent(
#     model="gpt-4.1-mini", middleware=[user_role_prompt], context_schema=Context
# )
# response = agent.invoke(
#     {"messages": [{"role": "user", "content": "Explain what is MCP servers"}]},
#     context=Context(user_role="child"),
# )
# print(response)

# embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# texts = [
#     "apple makes good computers,",
#     "i believe in pears",
#     "i thing lenovo is really good",
# ]
# load_dotenv()
# vector_store = FAISS.from_texts(texts, embedding=embeddings)

# print(vector_store.similarity_search("apples are my favourite food", k=7))
# print(vector_store.similarity_search("lenovo", k=7))


# retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# retriever_tool = create_retriever_tool(
#     retriever, name="kb_search", description="Search knowledge base for information"
# )

# agent = create_agent(
#     model="gpt-4.1-mini",
#     tools=[retriever_tool],
#     system_prompt="Helpful assistant. call your knowledge to answer the questions ",
# )

# result = agent.invoke(
#     {"messages": [{"role": "user", "content": "what fruits does person like"}]}
# )
# print(result)
# print(result["messages"][-1].content)


# ----------------------------------------


# @dataclass
# class Context:
#     user_id: str


# @dataclass
# class ResponseFormat:
#     summary: str
#     temperature_celcius: float
#     temperature_fahrenheit: float
#     humidity: float


# @tool("locate_user", description="Look up a users city based on the context")
# def locate_user(runtime: ToolRuntime[Context]):
#     match runtime.context.user_id:
#         case "ABC123":
#             return "Vienna"
#         case "123ABC":
#             return "Klagenfurt"
#         case _:
#             return "Unknown"


# @tool(
#     "get_weather",
#     description="Return weather information for a given city",
#     return_direct=False,
# )
# def get_weather(city: str):
#     response = requests.get(f"https://wttr.in/{city}?format=j1")
#     return response.json


# model = init_chat_model("gpt-4.1-mini", temperature=0.3)

# checkpointer = InMemorySaver()


# agent = create_agent(
#     model=model,
#     tools=[get_weather, locate_user],
#     system_prompt="You are a helpful assistant.",
#     context_schema=Context,
#     response_format=ResponseFormat,
#     checkpointer=checkpointer,
# )

# config = {"configurable": {"thread_id": 1}}
# response = agent.invoke(
#     {
#         "messages": [{"role": "user", "content": "what is the weather like?"}],
#     },
#     config=config,
#     context=Context(user_id="ABC123"),
# )

# print(response["structured_response"])
# print(response["structured_response"].summary)


# model = init_chat_model(model="gpt-4.1-mini", temperature=0.1)

# conversation = [
#     SystemMessage("You are a helpful assistant"),
#     HumanMessage("What is Python"),
#     AIMessage("Python is an intepreted programming language"),
#     HumanMessage("When it was released?"),
# ]
# response = model.invoke(conversation)

# print(response)
# print(response.content)


# model = init_chat_model("gpt-4.1-mini")

# message = {
#     "role": "user",
#     "content": [
#         {"type": "text", "text": "Describe the content of this image"},
#         {
#             "type": "image",
#             "url": "https://images.squarespace-cdn.com/content/v1/5ddfec9bdcb2647c79f8f404/1707256783640-88YGJZL67WE1U5AWUWSR/Band+Photo.png?format=1000w",
#         },
#     ],
# }

# response = model.invoke([message])
# print(response.content)


class HooksDemo(AgentMiddleware):
    def __init__(self):
        super().__init__()
        self.start_time = 0.0

    def before_agent(self, state: AgentState, runtime):
        self.start_time = time.time()
        print("before_agent triggered")


agent = create_agent("gpt-4.1-mini", middleware=[HooksDemo()])
