import time
from typing import List

import streamlit as st
from dotenv import load_dotenv
from interface import Interface
from load_policies import load_policies

load_dotenv()

if "message_history" not in st.session_state:
    st.session_state.message_history = []
else:
    st.session_state.message_history = st.session_state.message_history[-10:]

@st.cache_resource
def _load_policies(policy_path: str):
    return load_policies(policy_path)

@st.cache_resource
def load_and_add_policies(policies: List[str]):
    chatbot = Interface("hr_policies")
    for name, text in policies.items():
        chatbot.add_policy(name, text)
    return chatbot

def fake_streaming_response(response: str):    
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

policies = _load_policies("./Policies")
chatbot = load_and_add_policies(policies)

st.header("HR helper PoC")

for name, text in policies.items():
    with st.expander(f"Policy: {name}"):
        st.write(text)

for m in st.session_state.message_history:
    st.chat_message(m[0]).write(m[1])

prompt = st.chat_input("Ask")
if prompt:
    st.session_state.message_history.append(("user", prompt))
    st.chat_message("user").write(prompt)
    chatbot_response = chatbot.ask(prompt)
    st.chat_message("assistant").write_stream(fake_streaming_response(chatbot_response))
    st.session_state.message_history.append(("assistant", chatbot_response))
