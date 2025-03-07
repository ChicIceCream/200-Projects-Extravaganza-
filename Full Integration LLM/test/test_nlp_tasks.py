import streamlit as st
from src.nlp_tasks import init_chat_history, add_to_history, get_history_text

def test_chat_history():
    # Clear session state for testing
    if "chat_history" in st.session_state:
        st.session_state.chat_history.clear()
    else:
        st.session_state.chat_history = []
    
    init_chat_history()
    add_to_history("user", "Hello")
    add_to_history("assistant", "Hi there!")
    history = get_history_text()
    assert "User: Hello" in history
    assert "Assistant: Hi there!" in history
