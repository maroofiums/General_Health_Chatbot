# app.py
import os
import pickle
import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# ------------------- LOAD ENV -------------------
load_dotenv()  # loads .env
HF_TOKEN = os.getenv("HF_TOKEN")
if HF_TOKEN is None:
    st.error("HF_TOKEN not found in .env file. Please add it.")
    st.stop()

# ------------------- LOAD PROMPT BUNDLE -------------------
with open("prompts/health_prompt.pkl", "rb") as f:
    prompt_bundle = pickle.load(f)

SYSTEM_PROMPT = prompt_bundle["system_prompt"]
is_unsafe_question = prompt_bundle["safety_function"]

# ------------------- INITIALIZE HUGGING FACE CLIENT -------------------
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token=HF_TOKEN
)

# ------------------- STREAM RESPONSE FUNCTION -------------------
def stream_response(user_question):
    """
    Streams response from Hugging Face LLM.
    Handles unsafe questions with warning.
    """
    if is_unsafe_question(user_question):
        yield "⚠️ I can’t provide medical treatment or prescriptions. Please consult a qualified healthcare professional."
        return

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_question}
    ]

    stream = client.chat_completion(
        messages=messages,
        max_tokens=200,
        temperature=0.6,
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# ------------------- STREAMLIT UI -------------------
st.set_page_config(page_title="Health Chatbot", page_icon="🩺", layout="centered")

st.title("🩺 General Health Query Chatbot")
st.write("Ask general health-related questions. This chatbot does **not** replace a doctor.")

user_input = st.text_input("Enter your health question:")

if st.button("Ask"):
    if user_input.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            for token in stream_response(user_input):
                full_response += token
                response_placeholder.markdown(full_response)
