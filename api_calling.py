
import io
import streamlit as st

from google import genai
from dotenv import load_dotenv
from gtts import gTTS

import os



#load environment variables from .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

#initializing a client

genai_client = genai.Client(api_key=api_key)

#Note Generator

from PIL import Image # Add this import at the top

def note_generator(images):
    # Convert Streamlit UploadedFile objects to PIL Images
    pil_images = [Image.open(img) for img in images]
    
    prompt = """Summarize the picture in note format at max 100 words, 
    and make sure to include all the important points."""
    
    # Use the converted list 'pil_images'
    response = genai_client.models.generate_content(
        model="gemini-2.5-flash-lite", 
        contents=pil_images + [prompt] # Combine list of images with the prompt
    )
    
    return response.text


def audio_transcription(text):
    try:
        from gtts import gTTS
        import io
        
        audio_buffer = io.BytesIO()
        speech = gTTS(text=text, lang='en', slow=False)
        speech.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer
    except Exception as e:
        print(f"gTTS Error: {e}")
        return None
    
    
def quiz_generator(images, difficulty):
    # 1. Convert the Streamlit upload objects to PIL Images (The missing step!)
    pil_images = [Image.open(img) for img in images]
    
    prompt = f"""Generate 3 quizzes based on the provided images with {difficulty} difficulty. 
    Make sure to add markdown to differentiate the question and options. 
    Also make sure to include the correct answer in the quiz."""
    
    # 2. Use the converted pil_images list
    response = genai_client.models.generate_content(
        model="gemini-2.5-flash-lite", 
        contents=pil_images + [prompt] 
    )
    
    return response.text
