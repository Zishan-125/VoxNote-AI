import streamlit as st
from api_calling import note_generator
from api_calling import audio_transcription,quiz_generator
from PIL import Image

#title and description
st.title("Note Summary and Quiz Generator")
st.markdown("Upload upto 3 images to generate note summary and quiz questions.")
st.divider()

with st.sidebar:
    st.header("Upload Images")
    images = st.file_uploader(
        "Upload the photos of your note",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
    )
    
    if images:
        if len(images) > 3:
            st.error("Please upload a maximum of 3 images.")
        else:
            st.subheader("Uploaded Images")
            
            col= st.columns(len(images))

            
            for i,img in enumerate(images):
                with col[i]:
                    st.image(img)
                    
                    
       #difficulty

    selected_difficulty = st.selectbox(
         "Enter the difficulty level of the quiz questions",
         ("Easy", "Medium", "Hard"),
         index = None
         )
    
    
    
    pressed=st.button("Generate Note Summary and Quiz Questions",type="primary")
    
    
if pressed:
    if not images:
        st.error("Please upload at least one image to generate note summary and quiz questions.")
    if not selected_difficulty:
        st.error("Please select a difficulty level to generate quiz questions.")
        
    if images and selected_difficulty:
        
        #notes
        
        with st.container(border=True):
            st.subheader("Note Summary")
            
            #This portion will be replaced by API Call
        with st.spinner("Generating note summary..."):
            generated_note = note_generator(images)
            
            st.markdown(generated_note) # Changed from st.text to st.markdown
            
        #Audio
        
    with st.container(border=True):
            st.subheader("Audio Transcription")
            
            #This portion will be replaced by API Call
            with st.spinner("Generating Audio summary..."):
              generated_note =generated_note.replace("#","")
              generated_note =generated_note.replace("*","") 
              generated_note =generated_note.replace("-","")
              generated_note =generated_note.replace("`","")
              audio_transcript = audio_transcription(generated_note)
              st.audio(audio_transcript)
            
        #Quiz
        
    with st.container(border=True):
            st.subheader(f"Quiz ({selected_difficulty} Difficulty)")
            with st.spinner("Generating Quiz..."):
            #This portion will be replaced by API Call
             quizzes = quiz_generator(images,selected_difficulty)
             st.markdown(quizzes) # Changed from st.text to st.markdown
           