import streamlit as st

from st_iframe_postmessage import st_iframe_postmessage

st.title("Iframe postMessage")

st_iframe_postmessage(message={'event': "LOAD_COMPLETE"})

