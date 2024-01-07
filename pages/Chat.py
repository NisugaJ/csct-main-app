import json

import requests
import streamlit as st
import numpy as np

import streamlit as st
import random
import time

st.set_page_config(page_title="Chat with PlantaAI", page_icon='🌱', layout='wide')

st.title("Simple chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask PlantaAI"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display assistant response in chat message container
with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""

    if prompt:
        progress = st.progress(0)
        r = requests.post('http://127.0.0.1:5842/v1/query', json.dumps({'q': prompt}), stream=True)
        i = 1
        for chunk in r.iter_lines(decode_unicode=True, delimiter=' '):
            print(chunk)
            progress.progress(i)
            full_response += chunk + " "
            message_placeholder.markdown(full_response + "▌")
            i += 1

        message_placeholder.markdown(full_response)
    else:
        assistant_response = random.choice(
            ["Hello there! How can I assist you today?", "Hi there! Is there anything I can help you with?",
                "Do you need help?", ]
        )
        full_response = assistant_response
        st.markdown(assistant_response)

# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": full_response})