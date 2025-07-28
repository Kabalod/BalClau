
import streamlit as st
import requests

API_URL = "http://backend:8000"

st.title("Claude Agent Prompt Sender")

agent = st.text_input("Agent Name")
prompt = st.text_area("Prompt")

if st.button("Send Prompt"):
    response = requests.post(f"{API_URL}/agent/prompt", json={"agent": agent, "prompt": prompt})
    if response.status_code == 200:
        st.success("Response: " + response.json()["response"])
    else:
        st.error("Error: " + response.text)

if st.button("Show History"):
    response = requests.get(f"{API_URL}/agent/history/{agent}")
    if response.status_code == 200:
        for entry in response.json():
            st.write(entry)
    else:
        st.error("Error: " + response.text)
