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
