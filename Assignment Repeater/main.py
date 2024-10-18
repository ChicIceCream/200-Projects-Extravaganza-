import streamlit as st
import pyttsx3
import time

def speak_text(text, pause_duration):
    engine = pyttsx3.init()
    words = text.split()
    for word in words:
        engine.say(word)
        engine.runAndWait()
        time.sleep(pause_duration)

st.title("Assignment Repeater")
st.write("Type your text in the box below, adjust the pace, and click 'Speak' to hear it repeated.")

# Text input
user_input = st.text_area("Enter text:", height=100)

# Pace slider (inverse of speed)
pace = st.slider("Speech Pace", min_value=0.1, max_value=2.0, value=0.5, step=0.1)

# Speak button
if st.button("Speak"):
    if user_input.strip():
        speak_text(user_input, pace)
    else:
        st.warning("No text entered. Please type something and try again.")

st.write("To exit, simply close the browser tab or stop the Streamlit server.")
