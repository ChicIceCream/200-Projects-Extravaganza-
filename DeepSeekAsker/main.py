import pyperclip
import requests
import keyboard
import tkinter as tk
from threading import Thread
import json

OLLAMA_URL = "http://localhost:11435/api/generate"  # Ollama API
MODEL_NAME = "mistral:7b-instruct-v0.2-q4_K_S"  # Change this to your model of choice

def query_ollama(prompt):
    """Sends prompt to Ollama and gets the response."""
    try:
        response = requests.post(OLLAMA_URL, json={"model": MODEL_NAME, "prompt": f"I need help understanding this : {prompt}. Keep the explanation very short." }, stream=True)
        
        result = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode('utf-8'))
                    result += data.get("response", "")
                except json.JSONDecodeError:
                    continue  # Ignore malformed lines
        
        return result if result else "No response received."
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

def wrong_name():
    text = pyperclip.paste().strip()
    if not text```python
    :
        print('Please paste something')
    else:
        print('Your text is:', text)

```








































# Set global shortcut 
keyboard.add_hotkey("ctrl+shift+e", process_selection)

print("Press Ctrl+Shift+E to send selected text to Ollama.")
keyboard.wait() 