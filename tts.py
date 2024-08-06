from gtts import gTTS
import os

def text_to_speech(text, filename="tts.mp3"):
    # Create a gTTS object
    tts = gTTS(text, lang='en', slow=False)
    # Save the audio file
    tts.save(filename)

