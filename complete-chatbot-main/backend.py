from langchain_groq import ChatGroq
from dotenv import load_dotenv

from langgraph.graph import START, END, StateGraph
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

load_dotenv()
model = ChatGroq(model="moonshotai/kimi-k2-instruct")

from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver

# define state
class agentState(TypedDict):
    message : Annotated[list[BaseMessage], add_messages]

# define the function that perform the task
def chat_node(state:agentState):
    message = state['message']
    response = model.invoke(message)
    return {'message': [response]}
    
pointer = InMemorySaver()

# define the graph
graph = StateGraph(agentState)

# define the nodes
graph.add_node("chat_node", chat_node)

# define the edges
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# compile the graph
workflow = graph.compile(checkpointer= pointer)