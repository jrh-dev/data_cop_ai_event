import streamlit as st
from dotenv import load_dotenv
from helpers import (add_policies, cache_load_policies, create_chatbot,
                     tidy_title)

AVATAR = "https://clippyprofilepic.net/_next/image?url=https%3A%2F%2Ftest-icons.sparkiconai.com%2Fclippys%2F3d-clippy-original.webp&w=640&q=75"

load_dotenv()

st.set_page_config(
    page_title="HR Assistant Demo",
    page_icon=None,
    layout="wide",
    initial_sidebar_state=None,
    menu_items=None
)

hr_policy_chatbot = create_chatbot("hr_policies")


if "message_history" not in st.session_state:
    st.session_state.message_history = []
else:
    st.session_state.message_history = st.session_state.message_history[-10:]

policies, original_policies = cache_load_policies("./Policies")
add_policies(hr_policy_chatbot, policies)

st.header("HR helper PoC")

policies_col, chat_col = st.columns([3, 2])

with policies_col:
    st.subheader("Policies")

    for name, text in original_policies.items():
        with st.expander(f"{tidy_title(name)} Policy", expanded=False):
            st.write(text)

with chat_col:
    st.subheader("Ask virtual HR assistant")
    prompt = st.chat_input("Ask")
    for m in st.session_state.message_history:
        st.chat_message(m[0]).write(m[1])
    
    if prompt:
        st.session_state.message_history.append(("user", prompt))
        st.chat_message("user").write(prompt)
        with st.spinner("Thinking..."):
            chatbot_response = hr_policy_chatbot.ask(prompt)
        st.chat_message("assistant", avatar = AVATAR).write(chatbot_response)
        st.session_state.message_history.append(("assistant", chatbot_response))
