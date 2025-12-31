import os
import pickle
import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv() 
HF_TOKEN = os.getenv("HF_TOKEN")
if HF_TOKEN is None:
    st.error("HF_TOKEN not found in .env file. Please add it.")
    st.stop()

SYSTEM_PROMPT = """
You are a helpful and friendly medical assistant.
You only answer general health-related questions.

Rules:
- Do NOT provide medical diagnosis.
- Do NOT prescribe medicines or dosages.
- Avoid harmful or emergency medical advice.
- If the question is serious, politely advise seeing a doctor.
- Keep responses clear, calm, and friendly.
"""

def is_unsafe_question(text):
    blocked_words = [
        "dosage", "dose", "prescription",
        "how much medicine",
        "treatment for cancer",
        "suicide", "self harm"
    ]
    return any(word in text.lower() for word in blocked_words)


client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token=HF_TOKEN
)

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
st.set_page_config(page_title="Health Chatbot", page_icon="🩺", layout="centered")
st.title("🩺 General Health Query Chatbot")
st.write("Ask general health-related questions. This chatbot does **not** replace a doctor.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Enter your health question:")

if st.button("Ask") and user_input.strip():
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Display chat messages
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.chat_message("user").markdown(msg["content"])
        else:
            st.chat_message("assistant").markdown(msg["content"])

    # Add assistant placeholder for streaming
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        for token in stream_response(user_input):
            full_response += token
            response_placeholder.markdown(full_response)
    
    # Save assistant response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": full_response})
