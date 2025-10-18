import streamlit as st
from backend import workflow
from langchain_core.messages import HumanMessage, AIMessage
from typing import Any,cast

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = [{
        'role':'ai', 'message' : "Helpful assistant , ask anything to get suggestions from this chatbot"
    }]

st.title("Chatbot")

for message in st.session_state['chat_history']:
     with st.chat_message(message['role']):
            st.write(message['message'])

config1: Any = {'configurable':{
    'thread_id' : "thread-1"
}}

query = st.chat_input("Type something")

if query:
    st.session_state['chat_history'].append(
        {'role' : 'human', 'message' : query}
    )
    with st.chat_message('human'):
        st.write(query)

    initial_state:Any = {
        'message' : [HumanMessage(content=query)]
    }
    
    with st.chat_message('ai'):
        # response = st.write_stream(
        #     message_chunk.content for message_chunk, metadata in workflow.stream(
        #         initial_state,
        #         config= config1,
        #         stream_mode= 'messages'
        #     )
        # )
        response_parts = []
        def _stream_generator():
            for message_chunk, metadata in workflow.stream(
                initial_state,
                # config=config1,
                config = cast(Any, config1),
                stream_mode='messages'
            ):
                if isinstance(message_chunk, str):
                     text = message_chunk
                else:
                   # message_chunk may be an object with .content or already a string
                   text = getattr(message_chunk, "content", str(message_chunk))
                response_parts.append(text)
                yield text

        st.write_stream(_stream_generator())
        response = "".join(response_parts)
    st.session_state['chat_history'].append(
        {'role' : 'ai', 'message' : response}
    )
