from lyzr import VoiceBot
import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import zipfile

load_dotenv()
all_=[]
vb = VoiceBot(api_key="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")
genai.configure(api_key="AIzaSyBxbqUnQvC5tc5YLX_5CVIC-d_vEmHb1Ss")
model = genai.GenerativeModel('gemini-pro')

def upload():
    try:
        uploaded_file = st.file_uploader('Upload a zip file', type=["zip"])
        if uploaded_file is not None:
            return uploaded_file
        else:
            st.text("UPLOAD A FILE")
    except:
        pass
   
def extract_zip(file_path, extract_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            file_info.filename = os.path.basename(file_info.filename)
            zip_ref.extract(file_info, extract_path)
    
def transcribe(file):
    transcripts = []
    transcript = vb.transcribe(file)
    transcripts.append(transcript)
    return transcripts

def main():
    st.title("AUDIO ANALYZER")
    
    files = upload()
    bname = st.button("PROCESS")
    extract = r"C:\Users\amjat\Desktop\airlines voice\extracted"
    
    if bname:
        if files:
            extract_zip(files.name, extract)
            all_transcripts = []
            for file in os.listdir(extract):
                audio_file_path = os.path.join(extract, file)
                trans = transcribe(audio_file_path)
                all_transcripts.extend(trans)
            
            # Store the transcribed text in a list
            st.write("Transcriptions:")
            for trans in all_transcripts:
                st.write(trans)

            # Perform inference for each text
            prompt = '''Generate the output for the problem they are facing:

[User's input text goes here]
Find the magnitude of the below feature if your unable to do it infernce[Not mentioned in the text] some random value similar to the text
Features:
1) Provide me the output for the problem they are facing
2) Sentiment analysis for the text with the score
3) Key phrases in the text
4) KPI (Key Performance Indicators):
    1- 
        - Average handling time
        - First call resolution
        - Customer satisfaction
        - Call abandonment rate
        - Call resolution rate
        - Call transfer rate
        - Average speed of answer
        - Call rating
        - Silence ratio
        - Error rate
    2- Enterprise level KPI:
        - Service level
        - Time to solve the problem
        - Customer effort score
        - Contact quality
        - Agent satisfaction
        - Customer retention rate
        - Compliance adherence rate
    Find the magnitude of the below feature if your unable to do it infernce some random value similar to the text
Features:
'''
            for text in all_transcripts:
                # Combine prompt with transcribed text
                input_text = prompt.replace("[User's input text goes here]", text)
                # Perform inference using GenerativeAI model
                response = model.generate_content(input_text)
                all_.append(response)
                # Interpret the output for the specified features
                # You can extract and analyze the relevant information from response
                # and calculate the magnitude of the specified features
            st.write(all_)

if __name__ == "__main__":
    main()


