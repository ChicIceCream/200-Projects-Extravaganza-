import streamlit as st

st.title("Streamlit + Flask Inference")

st.markdown("""
    This Streamlit app embeds a Flask application that captures video from the camera,
    performs model inference, and streams the output.
    """)
    
# Embed the Flask app's page using an iframe (adjust the width/height as needed)
flask_app_url = "http://localhost:5000"
st.markdown(f'<iframe src="{flask_app_url}" width="700" height="600"></iframe>', unsafe_allow_html=True)
