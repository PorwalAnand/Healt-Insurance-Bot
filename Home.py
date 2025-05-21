import streamlit as st
from PIL import Image

st.set_page_config(page_title="Health Insurance Assistant", layout="wide")

# Logo and heading
logo = Image.open("assets/logo.png")
st.image(logo, width=160)

st.title("👋 Welcome to Your Health Insurance Assistant")
st.markdown("""
This assistant helps you with:
- 📋 Entry age & eligibility
- 🛡️ Coverage and policy features
- 📄 Claims, documents, and forms
- 💰 Premiums and installments
""")

st.image("assets/image.png", width=600)

# Optional: direct button to chatbot page
st.page_link("pages/💬 Chatbot.py", label="👉 Go to Chatbot")
