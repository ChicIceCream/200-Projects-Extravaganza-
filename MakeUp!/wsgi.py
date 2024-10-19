import streamlit.web.bootstrap as bootstrap
from app import makeup_app  # Import your MakeupApplication instance

def main():
    bootstrap.run(
        "app.py",
        "streamlit run",
        [],
        {}
    )

if __name__ == "__main__":
    main()
