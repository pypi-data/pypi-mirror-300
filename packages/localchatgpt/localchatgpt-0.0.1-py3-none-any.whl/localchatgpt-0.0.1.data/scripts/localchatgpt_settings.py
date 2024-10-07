import streamlit as st
from localchatgpt_init import *

def save_sm() -> None:
    modifySM(returnValue('system_message'))

st.title('Local Chat GPT Settings ⚙️')

with st.expander(label='**Set System Message** *(optional)*', expanded=False):
    st.session_state['system_message'] = st.text_area(label='Override system message', value=returnValue('system_message'), label_visibility="hidden", height=500, on_change=save_sm)
st.session_state['streaming_enabled'] = st.toggle(label='Enable Streaming', value=returnValue('streaming_enabled'))

with st.expander(label='**LLM Server Settings**', expanded=False, icon=":material/neurology:"):
    st.session_state['llm_server'] = st.text_input(label="LLM Server Host", value=returnValue('llm_server'))
    setLLMServer(returnValue('llm_server'))
    st.session_state['selected_model'] = st.selectbox('**Available Models**', placeholder="Choose an Option", options=getModelList())

def loadDefaultSettings():
    st.session_state['selected_model'] = st.selectbox('Models', placeholder="Choose an Option", options=getModelList(),label_visibility='hidden')