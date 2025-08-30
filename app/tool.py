from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
import requests


class State(MessagesState):
    my_var: str

def multiply(a: int, b: int) -> int:
    """Multiply two integers a and b
    
    Args:
        a: The first integer
        b: The second integer
    """
    return a * b
def add(a: int, b: int) -> int:
    """Add two integers a and b
    
    Args:
        a: The first integer
        b: The second integer
    """
    return a + b

def get_categories() -> str:
    """Get the categories of the products"""
    
    response = requests.get("https://api.escuelajs.co/api/v1/categories")
    categories = response.json()
    categories_names = [category["name"] for category in categories]
    
    return ", ".join(categories_names)
    

tools = [multiply, add, get_categories]

llm = ChatOpenAI(model='gpt-4o', temperature=0)
llm = llm.bind_tools(tools, parallel_tool_calls=False)

# Node
def assistant(state: State) -> State:
    system_message = SystemMessage(content="Eres un experto en categorias de productos y debes de ayudar a resolver problemas de categorias de productos y ademas eres un experto en matematicas y debes de ayudar a resolver problemas de matematicas")
    
    return {"messages": [llm.invoke( [system_message] + state['messages'])]}


builder = StateGraph(State)

builder.add_node('assistant', assistant)
builder.add_node('tools', ToolNode(tools))

builder.add_edge(START, 'assistant')
builder.add_conditional_edges('assistant',tools_condition)
builder.add_edge('tools', 'assistant')

graph = builder.compile()
