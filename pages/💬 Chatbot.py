import streamlit as st
import json
import os
import google.generativeai as genai
from rag_utils import prepare_embeddings, retrieve_context

# Set up Gemini model
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-flash")

st.set_page_config(page_title="Chatbot", layout="wide")
st.title("💬 Health Insurance Chatbot")

st.markdown("Ask me anything about your health insurance policy — coverage, plans, claims, documents, and more.")

# Suggested starter questions
with st.expander("💡 Try asking:"):
    st.markdown("""
    - What is the entry age?
    - What does the base plan cover?
    - What are the available premiums?
    - Do I need medical checkup?
    - What documents do I need for a claim?
    """)

# Load vectorstore once (from disk or rebuild if missing)
if "vectorstore" not in st.session_state:
    with open("assets/data.json") as f:
        data = json.load(f)
    st.session_state.vectorstore = prepare_embeddings(data)

# Chat history memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show past messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
query = st.chat_input("Ask about your insurance...")

if query:
    # Save and display user message
    st.chat_message("user").write(query)
    st.session_state.messages.append({"role": "user", "content": query})

    # RAG: Get context from FAISS
    docs = retrieve_context(query, st.session_state.vectorstore)
    context = "\n\n".join(docs)

    prompt = f"""You are a helpful insurance assistant. Use the context below to answer:

Context:
{context}

Question:
{query}"""

    # Generate response
    response = model.generate_content(prompt)
    answer = response.text

    # Display and save response
    st.chat_message("assistant").write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
