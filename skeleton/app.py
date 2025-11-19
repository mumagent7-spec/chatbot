import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Get the API key from environment variables
# The template.yaml will pass this in, and it will be in the .env file
groq_api_key = os.environ.get("GROQ_API_KEY")

# Check if the API key is available
if not groq_api_key or groq_api_key == "your-groq-api-key-here":
    st.error("Groq API key not found. Please add it to the .env file.")
    st.stop()

client = Groq(api_key=groq_api_key)

st.title("Insurance Chatbot")
st.caption("A friendly chatbot to help you with your insurance questions.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful general-purpose assistant. You should be friendly, professional, and provide clear and concise answers to questions."
        }
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What can I help you with?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Get response from Groq
        chat_completion = client.chat.completions.create(
            messages=st.session_state.messages,
            model="llama3-8b-8192", # Or another model you prefer
        )
        response = chat_completion.choices[0].message.content

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"An error occurred: {e}")
