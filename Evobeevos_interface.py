import openai
import streamlit as st
import pandas as pd
import numpy as np

st.title("EvoBeevos Variant Predictor 🐝")

st.header("**About**")

st.write("EvoBeevos is a comprehensive "
         "Variant Effect Predictor that leverages the Evo 2 AI model "
         "to predict genetic variant effects. It compares these predictions with "
         "ClinVar/dbSNP data, offering users a thorough analysis of variant significance. "
         "The app features a Streamlit interface, API integrations, a lightweight database "
         "for caching results, and an AI chatbot for user assistance.")

with st.form("uscs-form",clear_on_submit=False, enter_to_submit=True):
    st.write("Input chromosome address in UCSC format")
    chromosome_number = st.number_input("Chromosome Number")
    starting_base_pair = st.text_input("Starting Base Pair")
    ending_base_pair = st.text_input("Ending Base Pair")
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("Chromosome number",chromosome_number,
                 "Starting BP", starting_base_pair,
                 "Ending BP", ending_base_pair
                 )


# openAi chatbot
st.title("EvoBeevos Chatbot 🤖")

api_key = st.secrets['openai']['api_key']

openai.api_key = api_key

if "openai_model" not  in st.session_state:
    st.session_state.openai_model = "gpt-3.5-turbo"
# with st.chat_message(name="assistant"):
    # st.write("Hello! I am EvoBeevos, your friendly AI chatbot. How can I help you today?")'''

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message(name="user"):
        st.markdown(prompt)
    # Store user message in chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response from OpenAI
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages   
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "|")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})   

            





# Display result and score on main page
# Display CliVar comparison on main page as well?
# Sidebar will have user input info, or should it also be on main page
# Where to put chatbot?
# What kind of input do we want the user to put in (i.e DNA sequences? Should we cap how long the sequence can be?)
