import streamlit as st

main_page = st.Page("localchatgpt_home.py", title="Home", icon="🏠")
settings_page = st.Page("localchatgpt_settings.py", title="Settings", icon="⚙️")

pg = st.navigation([main_page, settings_page])
#st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()
