import streamlit as st
import pandas as pd
import numpy as np

st.title("EvoBeevos Variant Predictor 🐝")

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


# Display result and score on main page
# Display CliVar comparison on main page as well?
# Sidebar will have user input info, or should it also be on main page
# Where to put chatbot?
# What kind of input do we want the user to put in (i.e DNA sequences? Should we cap how long the sequence can be?)
