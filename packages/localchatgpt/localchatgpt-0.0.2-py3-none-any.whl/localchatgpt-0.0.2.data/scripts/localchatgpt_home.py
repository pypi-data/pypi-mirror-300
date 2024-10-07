import streamlit as st
from localchatgpt_init import *
import time
from streamlit_extras.tags import tagger_component

st.set_page_config(page_title='Local Chat GPT', page_icon='⚛')

localchatgpt_avatar = "⚛️"

def resetChat():
    returnValue('messages').clear()
    clearHistory()

with st.sidebar:
    st.metric("Selected Model ✅", returnValue('selected_model'))
    st.metric("Connected to 🔌", returnValue('llm_server'))
    st.metric("Streaming 🔄", returnValue('streaming_enabled'))

# set default system message
setSM(returnValue('system_message'))

st.markdown('# :rainbow[Local Chat GPT] ⚛️')

with st.chat_message(name='assistant', avatar=localchatgpt_avatar):
    st.markdown('Chat with me..')
for message in returnValue('messages'):
    with st.chat_message(name=message['role'], avatar = localchatgpt_avatar if message['role'] == 'assistant' else None):
        st.markdown(message['content'])
if prompt := st.chat_input('Enter your prompt'):
    returnValue('messages').append({'role' : 'user', 'content' : prompt})
    with st.chat_message(name='user'):
        st.markdown(prompt)
    with st.chat_message(name='assistant', avatar=localchatgpt_avatar):
        with st.spinner('Processing....'):
            full_response = chatWithModel(prompt=prompt, model=returnValue('selected_model'))
            returnValue('messages').append({'role' : 'assistant', 'content' : full_response})
            if st.session_state['streaming_enabled']:
                message_placeholder = st.empty()
                streaming_response = ""
                # Simulate stream of response with milliseconds delay
                for chunk in full_response.split():
                    streaming_response += chunk + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(streaming_response + "▌", unsafe_allow_html=True)
                message_placeholder.markdown(full_response, unsafe_allow_html=True)
            else:
                st.markdown(full_response)
    st.button('Reset Chat 🗑️', use_container_width=True, on_click=resetChat)