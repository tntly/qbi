
from groq import Groq
from typing import Generator
import streamlit as st
import pandas as pd
import numpy as np
from clinvar import get_clinvar_data

st.title("EvoBeevos Variant Predictor 🐝")

st.header("**About**")

st.write("EvoBeevos is a comprehensive "
         "Variant Effect Predictor that leverages the Evo 2 AI model "
         "to predict genetic variant effects. It compares these predictions with "
         "ClinVar/dbSNP data, offering users a thorough analysis of variant significance. "
         "The app features a Streamlit interface, API integrations, a lightweight database "
         "for caching results, and an AI chatbot for user assistance.")

with st.form("uscs-form",clear_on_submit=False, enter_to_submit=True):
    st.write("Input gene location")
    chromosome_number = st.number_input("Chromosome Number", min_value=0, step=1)
    starting_base_pair = st.number_input("Starting Base Pair",min_value=0, step=1)
    ending_base_pair = st.number_input("Ending Base Pair",min_value=0, step=1)
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("Chromosome number",chromosome_number,
                 "Starting BP", starting_base_pair,
                 "Ending BP", ending_base_pair,)
        
        ucsc_input = f"chr{chromosome_number}:{starting_base_pair}-{ending_base_pair}"
        st.write( "UCSC format",ucsc_input)
        result = get_clinvar_data(ucsc_input)
        if result["vars"]:
            variant_df = result["vars"]
            df = pd.DataFrame(variant_df)
            st.dataframe(df, use_container_width=True)


st.write("EvoBeevos is a comprehensive "
         "Variant Effect Predictor that leverages the Evo 2 AI model "
         "to predict genetic variant effects. It compares these predictions with "
         "ClinVar/dbSNP data, offering users a thorough analysis of variant significance. "
         "The app features a Streamlit interface, API integrations, a lightweight database "
         "for caching results, and an AI chatbot for user assistance.")

# Display result and score on main page
# Display CliVar comparison on main page as well?
# Sidebar will have user input info, or should it also be on main page
# Where to put chatbot?
# What kind of input do we want the user to put in (i.e DNA sequences? Should we cap how long the sequence can be?)
st.title("EvoBeevos Chatbot 🤖")
# openAi chatbot
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"],
)

# Initialize chat history and selected model
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

# Define model details
models = {
    "gemma2-9b-it": {"name": "Gemma2-9b-it", "tokens": 8192, "developer": "Google"},
    "llama-3.3-70b-versatile": {"name": "LLaMA3.3-70b-versatile", "tokens": 128000, "developer": "Meta"},
    "llama-3.1-8b-instant" : {"name": "LLaMA3.1-8b-instant", "tokens": 128000, "developer": "Meta"},
    "llama3-70b-8192": {"name": "LLaMA3-70b-8192", "tokens": 8192, "developer": "Meta"},
    "llama3-8b-8192": {"name": "LLaMA3-8b-8192", "tokens": 8192, "developer": "Meta"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
}

# Layout for model selection and max_tokens slider
col1, col2 = st.columns(2)

with col1:
    model_option = st.selectbox(
        "Choose a model:",
        options=list(models.keys()),
        format_func=lambda x: models[x]["name"],
        index=4  # Default to mixtral
    )

# Detect model change and clear chat history if model has changed
if st.session_state.selected_model != model_option:
    st.session_state.messages = []
    st.session_state.selected_model = model_option

max_tokens_range = models[model_option]["tokens"]

with col2:
    # Adjust max_tokens slider dynamically based on the selected model
    max_tokens = st.slider(
        "Max Tokens:",
        min_value=512,  # Minimum value to allow some flexibility
        max_value=max_tokens_range,
        # Default value or max allowed if less
        value=min(32768, max_tokens_range),
        step=512,
        help=f"Adjust the maximum number of tokens (words) for the model's response. Max for selected model: {max_tokens_range}"
    )

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


if prompt := st.chat_input("Enter your prompt here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='👨‍💻'):
        st.markdown(prompt)

    # Fetch response from Groq API
    try:
        chat_completion = client.chat.completions.create(
            model=model_option,
            messages=[
                {
                    "role": m["role"],
                    "content": m["content"]
                }
                for m in st.session_state.messages
            ],
            max_tokens=max_tokens,
            stream=True
        )

        # Use the generator function with st.write_stream
        with st.chat_message("assistant", avatar="🤖"):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)
    except Exception as e:
        st.error(e, icon="🚨")

    # Append the full response to session_state.messages
    if isinstance(full_response, str):
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response})
    else:
        # Handle the case where full_response is not a string
        combined_response = "\n".join(str(item) for item in full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": combined_response})


