import speech_recognition as sr

# Path to the uploaded audio file
audio_path = "C:\Users\User\Downloads\WhatsApp Audio 2025-03-21 at 12.46.02_1a1f3330.mp3"
# Initialize recognizer
recognizer = sr.Recognizer()

# Load and transcribe the audio file
with sr.AudioFile(audio_path) as source:
    audio_data = recognizer.record(source)  # Record the entire audio
    try:
        transcription = recognizer.recognize_google(audio_data)  # Use Google's speech recognition
    except sr.UnknownValueError:
        transcription = "Could not understand the audio."
    except sr.RequestError:
        transcription = "Speech recognition service unavailable."

transcription
