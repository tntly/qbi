from groq import Groq
from typing import Generator
import streamlit as st
import pandas as pd

st.title("EvoBeevos Variant Predictor 🐝")

st.header("**About**")

st.write("EvoBeevos Variant Predictor is a comprehensive "
         "Variant Effect Predictor that leverages the Evo 2 AI model "
         "to predict genetic variant effects. It compares these predictions with "
         "ClinVar/dbSNP data, and Ensemble data, offering users a thorough analysis of variant significance. "
         "The app features a Streamlit interface, API integrations, and an AI chatbot for user assistance.")

# User input form
with st.expander("**User input form**"):
    with st.form("uscs-form",clear_on_submit=False):
        st.write("Input gene location")
        chromosome_number = st.number_input("Chromosome Number",min_value=0, step=1, value=17)
        base_pairs = ['A', 'T', 'C', 'G']
        mutation_position = st.number_input("Mutation position", min_value=0, step=1,value=41276133)
        original_allele = st.selectbox("Enter original base pair", base_pairs)
        mutated_allele = st.selectbox("Enter mutated base pair", base_pairs)
        submitted = st.form_submit_button("Submit")
# Processing input and displaying results
if submitted:
    ucsc_input = f"chr{chromosome_number}:{mutation_position}{original_allele}>{mutated_allele}"
    st.write(f"**UCSC Format:** {ucsc_input}")

    # Placeholder result
    evo2_result = "Likely to cause LOF" # placeholder
    evo2_delta_score = 0.000299

    ensemble_result = [
        "Gene id:'ENSG00000180386'",
        "Consequence terms: stop_gained",
        "biotype: protein_coding",
        "impact: HIGH"
    ] # placeholder

    clinvar_conditions = [
        "Inborn_genetic_diseases",
        "Hereditary_cancer-predisposing_syndrome",
        "Cardiovascular_phenotype",
        "Primary_ciliary_dyskinesia",
        "Inborn_genetic_diseases|not_provided"
    ] # placeholder for clinvar conditions
    
    with st.expander("**Prediction Results**"):
        # Evo model result
        st.subheader("Evo2 Model Prediction")
        st.write(f"**Result: **{evo2_result}")
        st.write(f"**Delta Score: **{evo2_delta_score}")

        # Ensemble model result
        st.subheader("Ensemble Data")
        st.write("**Result: **")
        for item in ensemble_result:
            st.write(f"- {item}")
        
        # ClinVar conditions
        st.subheader("Top 5 Conditions from ClinVar")
        for condition in clinvar_conditions:
            st.write(f"- {condition}")      

# Groq Chatbot
st.header("EvoBeevos Chatbot 🤖")

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"],
)
# Define the Groq Ai's initial instruction
system_message = {
    "role": "system",
    "content": (
        "You are EvoBeevos, an AI expert in genetic variant analysis."
        "Help users understand genetic mutations by analyzing ClinVar data and dbDNP data."
        "You can also provide information on genetic variants and their effects."
        "You can also provide information on the gene, its function, and the effects of the mutation on it."
        "Provide concise and expert level information to users."
        "Step 1: Identify the gene and its biological function."
        "Step 2: Analyze the effect of the mutation on the protein."
        "Step 3: Check conservation across species."
        "Step 4: Reference ClinVar or other databases for known classifications."
        "Step 5: Conclude with a classification and justification."
        "### Example 1:"
        "Variant: TP53 c.215C>G"
        "**Step 1:** TP53 is a tumor suppressor gene involved in apoptosis and DNA repair." 
        "**Step 2:** This mutation results in an R72P substitution, altering protein structure."  
        "**Step 3:** Arginine at position 72 is highly conserved across mammals."  
        "**Step 4:** Prior research suggests this variant may impair apoptosis, making it potentially pathogenic." 
        "**Step 5:** Conclusion: *Likely Pathogenic* (based on conservation and functional impact)." 

    )
}

# Initialize chat history and selected model
if "messages" not in st.session_state:
    st.session_state.messages = [system_message]

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
    temper = st.slider(
            "Temperature:",
            min_value=0.0,  # Minimum value to allow some flexibility
            max_value=1.0,
            step=0.05,
            help=f"Adjust the temperature for the model's response. Lower temperatures are highly structured while higher temperatures are more creative."
        )
    top_p = st.slider(
        "Top_p:",
        min_value=0.0,  # Minimum value to allow some flexibility
        max_value=1.0,
        step=0.05,
        help=f"Adjust the top-p for the model's response. Lower values of top-p make a more structured and focused model while higher temperatures are more diverse."
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
            temperature=temper,
            top_p=top_p,
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


