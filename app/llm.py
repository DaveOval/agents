from langchain_openai import ChatOpenAI
from typing import TypedDict
from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END

llm = ChatOpenAI(model='gpt-4o', temperature=0)
# llm.invoke("Hello, world!")

# Define the state of the agent
class State(MessagesState):
    my_var: str
    customer_name: str
    

system_message = SystemMessage(content="You are a helpful assistant and you are a expertin in React, only respond about React, avoid answering about other topics")

# Node
def node_llm(state: State) -> State:
    print(state)
    return {"messages": [llm.invoke( [system_message] + state['messages'])]}


builder = StateGraph(State)

builder.add_node('node_llm', node_llm)

builder.add_edge(START, 'node_llm')
builder.add_edge('node_llm', END)

graph = builder.compile()