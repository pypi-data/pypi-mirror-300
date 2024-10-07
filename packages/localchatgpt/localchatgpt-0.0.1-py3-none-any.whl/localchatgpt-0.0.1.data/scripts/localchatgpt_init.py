import streamlit as st
from localchatgpt_prompt import *

DEFAULT_SYSTEM_MESSAGE = """
        You are a helper assistant
"""

default_settings = {
    'streaming_enabled' : False,
    'messages' : [],
    'system_message' : DEFAULT_SYSTEM_MESSAGE,
    'selected_model' : getModelList()[0],
    'llm_server' : "127.0.0.1",
}

def returnValue(key):
    if key not in st.session_state:
        st.session_state[key] = default_settings[key]
    return st.session_state[key]

