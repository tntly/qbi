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
