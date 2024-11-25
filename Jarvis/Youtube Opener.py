import speech_recognition as sr
import pyttsx3
import webbrowser
import time

class VoiceAssistant:
    def __init__(self):
        # Initialize the speech recognizer and text-to-speech engine
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        # Get available voices
        voices = self.engine.getProperty('voices')
        # Set female voice - usually the second voice in the system
        for voice in voices:
            # Look for a female voice
            if "female" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
            # Fallback to the second voice if no explicit female voice is found
            elif voices.index(voice) == 1:
                self.engine.setProperty('voice', voice.id)
        
        # Adjust voice properties
        self.engine.setProperty('rate', 145)     # Slightly slower rate
        self.engine.setProperty('volume', 0.9)   # Volume level
        self.engine.setProperty('pitch', 1.1)    # Slightly higher pitch
        
        # Wake word
        self.wake_word = "computer"
        
    def speak(self, text):
        """Convert text to speech"""
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        
    def listen(self):
        """Listen for voice input and convert to text"""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {text}")
                return text
            except sr.WaitTimeoutError:
                print("No speech detected")
                return ""
            except sr.UnknownValueError:
                print("Could not understand audio")
                return ""
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return ""
                
    def process_command(self, command):
        """Process the voice command"""
        while True:
            if "youtube" in command:
                self.speak("Opening YouTube for you now")
                webbrowser.open("https://www.youtube.com")
                return True
            elif "google" in command:
                self.speak("I'll open Google right away")
                webbrowser.open("https://www.google.com")
                return True
            elif "spotify" in command:
                self.speak("Opening Spotify for your listening pleasure")
                webbrowser.open("https://www.spotify.com")
                return True
            elif "exit" in command or "stop" in command:
                self.speak("Goodbye! Have a wonderful day")
                return False
            else:
                self.speak("I didn't quite catch that. Could you please try again?")
                command = self.listen()
        
    def run(self):
        """Main loop of the voice assistant"""
        self.speak("Hello! I'm your voice assistant. Just say 'computer' and I'll be here to help.")
        
        while True:
            print("\nWaiting for wake word...")
            command = self.listen()
            
            if not command:
                continue
                
            if self.wake_word in command:
                self.speak("Yes, how may I assist you?")
                
                command = self.listen()
                
                if command:
                    should_continue = self.process_command(command)
                    if not should_continue:
                        break
                else:
                    self.speak("I didn't hear your command. Please try again.")

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()