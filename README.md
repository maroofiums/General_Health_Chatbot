

# General Health Query Chatbot

[Live Demo](https://general-health-chatbot.streamlit.app/) | [Kaggle Notebook](https://www.kaggle.com/code/maroofiums/general-health-chatbot/) | [GitHub Repository](https://github.com/maroofiums/General_Health_Chatbot)

---

## Project Overview

This project implements a **General Health Query Chatbot** using **Large Language Models (LLMs)**. The chatbot is designed to answer general health-related questions in a **friendly and safe manner**, without providing medical diagnosis or prescriptions.

It showcases **prompt engineering, LLM API integration, real-time streaming, and user-friendly chat interface design**.

---

## Features

* **Friendly AI Interaction:** Chat interface similar to ChatGPT.
* **Prompt Engineering:** System prompt ensures professional, safe, and informative responses.
* **Safety Filters:** Blocks unsafe questions related to dosages, prescriptions, or serious medical emergencies.
* **Streaming Responses:** Answers appear token-by-token to simulate real-time conversation.
* **Session-based Chat History:** Maintains conversation context across multiple questions.
* **Deployment Ready:** Fully functional on Streamlit with Hugging Face LLM backend.

---

## Tools & Technologies

* **Python 3.13**
* **Streamlit** for frontend and UI
* **Hugging Face Inference API** with Mistral-7B-Instruct
* **Pickle** for prompt and safety function storage (optional)
* **Environment Variables** for secure API key management
* **Pathlib** for cross-platform file handling

---

## Implementation Details

1. **Prompt & Safety Function**

   * System prompt instructs the model to act as a friendly medical assistant.
   * Safety function prevents responses for unsafe queries.

2. **LLM Integration**

   * Hugging Face `InferenceClient` interacts with Mistral-7B-Instruct.
   * Streaming API used to display real-time responses in chat.

3. **Frontend & UI**

   * Streamlit chat interface with user and AI messages.
   * Chat history maintained using `st.session_state`.

---

## Challenges & Fixes

* **Duplicate Responses in UI:**
  Initially, the assistant response appeared twice. Fixed by **streaming directly inside a single `st.chat_message` block** and storing chat history in session state.

* **Pickle Loading Errors:**
  Using relative paths with `pathlib` solved issues when loading system prompts and safety functions from pickle.

* **API Key Management:**
  Streamlit Cloud rejected invalid `.env` secrets. Resolved by using Streamlit **Secrets Management** properly.

* **Token Streaming & Performance:**
  Ensured streaming responses work smoothly without freezing the UI.

---

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/maroofiums/General_Health_Chatbot.git
   cd General_Health_Chatbot
   ```

2. Install requirements:

   ```bash
   pip install -r requirements.txt
   ```

3. Set Hugging Face token (locally in `.env` or via Streamlit secrets):

   ```bash
   HF_TOKEN=your_huggingface_api_key
   ```

4. Run Streamlit app:

   ```bash
   streamlit run app.py
   ```

5. Ask general health questions in the chat interface.

---

## Project Outcome

* Implemented a **safe, interactive health chatbot**.
* Learned **prompt engineering**, **API integration**, and **real-time streaming** techniques.
* Overcame challenges with **UI duplication, API secrets, and file handling**.
* Ready for deployment on **Streamlit and Kaggle environments**.

---

## Links

* **Live Demo:** [https://general-health-chatbot.streamlit.app/](https://general-health-chatbot.streamlit.app/)
* **Kaggle Notebook:** [https://www.kaggle.com/code/maroofiums/general-health-chatbot/](https://www.kaggle.com/code/maroofiums/general-health-chatbot/)
* **GitHub Repo:** [https://github.com/maroofiums/General_Health_Chatbot](https://github.com/maroofiums/General_Health_Chatbot)
