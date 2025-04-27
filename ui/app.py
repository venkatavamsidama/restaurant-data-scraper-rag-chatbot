import sys
import os
os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"

# Fix for Streamlit + Torch issue (ensure torch.classes doesn't cause errors)
if "torch.classes" in sys.modules:
    del sys.modules["torch.classes"]

import streamlit as st
import torch

# Optional: Set number of threads to 1 to avoid multithreading issues
torch.set_num_threads(1)

# You can uncomment this line if you need multiprocessing support
# import multiprocessing
# multiprocessing.set_start_method('spawn')

# Add the parent directory to the sys.path for module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your chatbot interface
from rag_chatbot.interface import Chatbot

# Set up the Streamlit page configuration
st.set_page_config(page_title='Restaurant RAG Chatbot')

# Initialize chatbot
chatbot = Chatbot()

# Streamlit UI components
st.title('🍽️ Restaurant RAG Chatbot')
user_input = st.text_input('Ask about restaurant menus...')
if st.button('Send') and user_input:
    with st.spinner('Fetching answer...'):
        response = chatbot.ask(user_input)
    st.markdown(f"**Bot:** {response}")
