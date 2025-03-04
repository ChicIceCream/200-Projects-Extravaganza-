import cv2
from PIL import Image
import io
import tkinter as tk
from tkinter import Text, Label, Button, END
import threading

import google.generativeai as genai

# Configure the Gemini API (you'll need to get your own API key)
GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera with Gemini Vision")
        
        # Create UI
        self.camera_label = Label(root)
        self.camera_label.pack(padx=10, pady=10)
        
        self.capture_btn = Button(root, text="Analyze What's on Screen", command=self.capture_and_analyze)
        self.capture_btn.pack(pady=10)
        
        self.result_text = Text(root, height=10, width=50)
        self.result_text.pack(padx=10, pady=10)
        
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.result_text.insert(END, "Error: Could not open camera.")
            return
        
        # Set up Gemini model
        self.model = genai.GenerativeModel('gemini-pro-vision')
        
        # Start video stream
        self.update_frame()
    
    def update_frame(self):
        ret, self.frame = self.cap.read()
        if ret:
            # Convert frame for display
            display_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            h, w, _ = display_frame.shape
            photo = tk.PhotoImage(data=cv2.imencode('.ppm', display_frame)[1].tobytes())
            self.camera_label.configure(image=photo, width=w, height=h)
            self.camera_label.image = photo
        
        # Continue updating
        self.root.after(10, self.update_frame)
    
    def capture_and_analyze(self):
        if hasattr(self, 'frame'):
            self.result_text.delete(1.0, END)
            self.result_text.insert(END, "Analyzing what's on screen...")
            self.root.update_idletasks()
            
            # Process in separate thread to keep UI responsive
            threading.Thread(target=self.analyze_with_gemini).start()
    
    def analyze_with_gemini(self):
        try:
            # Convert OpenCV frame to format Gemini can use
            rgb_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_frame)
            
            # Convert to bytes
            img_byte_arr = io.BytesIO()
            pil_img.save(img_byte_arr, format='JPEG')
            img_bytes = img_byte_arr.getvalue()
            
            # Send to Gemini API
            response = self.model.generate_content(
                ["Describe what you see in this image.", img_bytes]
            )
            
            # Display result
            def update_ui():
                self.result_text.delete(1.0, END)
                self.result_text.insert(END, response.text)
            self.root.after(0, update_ui)
        except Exception as e:
            def show_error():
                self.result_text.delete(1.0, END)
                self.result_text.insert(END, f"Error: {str(e)}")
            self.root.after(0, show_error)
    
    def on_close(self):
        if self.cap.isOpened():
            self.cap.release()
        self.root.destroy()

# Start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()