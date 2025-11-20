import time
from typing import List
import streamlit as st
from load_policies import load_policies
from interface import Interface

def tidy_title(name: str) -> str:
    return name.replace("_", " ").title()

@st.cache_resource
def create_chatbot(name: str) -> Interface:
    return Interface(name)

@st.cache_resource
def cache_load_policies(policy_path: str):
    return load_policies(policy_path)

@st.cache_resource
def add_policies(_chatbot: Interface, policies: List[str]):
    for name, text in policies.items():
        if text.strip():
            _chatbot.add_policy(name, text)

def fake_streaming_response(response: str):    
    for word in response.split():
        yield word + " "
        time.sleep(0.05)