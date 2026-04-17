import io
import os
import time
import streamlit as st
from PIL import Image
from google import genai
from gtts import gTTS

# --- 1. SECURE API INITIALIZATION ---
# This ensures the code works both locally (.env) and on Streamlit Cloud (Secrets)
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Missing API Key. Please configure GEMINI_API_KEY in Secrets or .env.")
    st.stop()

# Initializing the Google GenAI client
genai_client = genai.Client(api_key=api_key)


# --- 2. NOTE GENERATOR ---
def note_generator(images):
    """Processes images and returns a structured summary."""
    try:
        pil_images = [Image.open(img) for img in images]
        
        prompt = """Summarize the picture in note format at max 100 words. 
        Focus on extracting key concepts, dates, and definitions. 
        Use bullet points for readability."""
        
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=pil_images + [prompt]
        )
        return response.text
    except Exception as e:
        return f"Error generating notes: {str(e)}"


# --- 3. AUDIO TRANSCRIPTION (WITH RETRY LOGIC) ---
def audio_transcription(text):
    """Converts text to speech using gTTS with error handling."""
    # Max 3 attempts to handle 'Failed to connect' network spikes
    for attempt in range(3):
        try:
            audio_buffer = io.BytesIO()
            speech = gTTS(text=text, lang='en', slow=False)
            speech.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            return audio_buffer
        except Exception as e:
            if attempt < 2:
                time.sleep(2)  # Wait 2 seconds before retrying
                continue
            print(f"gTTS Error after 3 attempts: {e}")
            return None


# --- 4. QUIZ GENERATOR ---
def quiz_generator(images, difficulty):
    """Generates 3 multiple-choice questions based on image content."""
    try:
        pil_images = [Image.open(img) for img in images]
        
        prompt = f"""Generate 3 quizzes based on the provided images with {difficulty} difficulty. 
        Format as follows:
        **Question X:** [The question]
        - A) [Option]
        - B) [Option]
        - C) [Option]
        - D) [Option]
        
        **Correct Answer:** [The letter]
        """
        
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=pil_images + [prompt] 
        )
        return response.text
    except Exception as e:
        return f"Error generating quiz: {str(e)}"
