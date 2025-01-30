import pyperclip
import requests
import keyboard
import tkinter as tk
from threading import Thread

OLLAMA_URL = "http://localhost:5000/api/generate"  # Ollama API
MODEL_NAME = "deepseek-r1:8b"  # Change this to your model

def query_ollama(prompt):
    """Sends prompt to Ollama and gets the response."""
    try:
        response = requests.post(OLLAMA_URL, json={"model": MODEL_NAME, "prompt": prompt})
        return response.json().get("response", "No response received.")
    except Exception as e:
        return f"Error: {e}"

def show_response(text):
    """Displays response in a new window."""
    window = tk.Tk()
    window.title("AI Response")

    text_widget = tk.Text(window, wrap="word", font=("Arial", 12))
    text_widget.insert("1.0", text)
    text_widget.pack(expand=True, fill="both")

    window.mainloop()

def process_selection():
    """Gets text from clipboard, queries AI, and shows result."""
    text = pyperclip.paste().strip()
    if not text:
        return
    
    response = query_ollama(text)
    
    # Show result in a separate thread (so it doesn't block)
    Thread(target=show_response, args=(response,), daemon=True).start()

# Set global shortcut (change as needed)
keyboard.add_hotkey("ctrl+shift+e", process_selection)

print("Press Ctrl+Shift+E to send selected text to Ollama.")
keyboard.wait()  # Keep script running
