from dotenv import load_dotenv
from typing import Annotated, List, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

load_dotenv()


llm = init_chat_model("gpt-4.1-mini")


# class State(TypedDict):
#     messages: Annotated[list, add_messages]


# graph_buldier = StateGraph(State)


# def chatbot(state: State):
#     return {"messages": [llm.invoke(state["messages"])]}


# graph_buldier.add_node("chatbot", chatbot)
# graph_buldier.add_edge(START, "chatbot")
# graph_buldier.add_edge("chatbot", END)

# graph = graph_buldier.compile()


# user_input = input("Enter a messages: ")
# state = graph.invoke({"messages": [{"role": "user", "content": user_input}]})
# print(state["messages"][-1].content)
class MessageClassifier(BaseModel):
    message_type: Literal["emotional", "logical"] = Field(
        ...,
        description="Classify if the message requires emotional or logical response",
    )


class State(TypedDict):
    messages: Annotated[List, add_messages]
    message_type: str | None


def classify_message(state: State):
    last_message = state["messages"][-1]
    classifier_llm = llm.with_structured_output(MessageClassifier)
    result = classifier_llm.invoke(
        [
            {
                "role": "system",
                "content": "Choose if user message is emotional or logical. Respond with only emotional or logical",
            },
            {"role": "user", "content": last_message.content},
        ]
    )
    return {"message_type": result.message_type}


def therapist_agent(state: State):
    last_message = state["messages"][-1]
    messages = [
        {
            "role": "system",
            "content": "You are a therapist. Respond to the user message with empathy and understanding.",
        },
        {"role": "user", "content": last_message.content},
    ]
    reply = llm.invoke(messages)
    return {"messages": [{"role": "assistant", "content": reply.content}]}


def logical_agent(state: State):
    last_message = state["messages"][-1]
    messages = [
        {
            "role": "system",
            "content": "You are a logical assistant. Respond to the user message with facts and logic.",
        },
        {"role": "user", "content": last_message.content},
    ]
    reply = llm.invoke(messages)
    return {"messages": [{"role": "assistant", "content": reply.content}]}


def router(state: State):
    message_type = state.get("message_type", "logical")
    if message_type == "emotional":
        return {"next": "therapist"}
    return {"next": "logical"}


graph_builder = StateGraph(State)
graph_builder.add_node("router", router)

graph_builder.add_node("classifier", classify_message)
graph_builder.add_node("therapist", therapist_agent)
graph_builder.add_node("logical", logical_agent)

graph_builder.add_edge(START, "classifier")
graph_builder.add_edge("classifier", "router")
graph_builder.add_conditional_edges(
    "router",
    lambda state: state.get("next"),
    {"therapist": "therapist", "logical": "logical"},
)
graph_builder.add_edge("therapist", END)
graph_builder.add_edge("logical", END)
graph = graph_builder.compile()


def run_chatbot():
    state = {"messages": [], "message_type": None}

    while True:
        user_input = input("Mesage:")
        if user_input == "exit":
            print("bye")
            break

        state["messages"] = state.get("messages", []) + [
            {"role": "user", "content": user_input}
        ]

        state = graph.invoke(state)
        if state.get("messages") and len(state["messages"]) > 0:
            last_messages = state["messages"][-1]
            print(f"Assistant: {last_messages.content}")


if __name__ == "__main__":
    run_chatbot()
