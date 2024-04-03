import streamlit as st
from lyzr import VoiceBot
import os
import zipfile
import re
from dotenv import load_dotenv
from google.generativeai import genai

load_dotenv()
all_results = []

vb = VoiceBot(api_key="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")
genai.configure(api_key="YOUR_GENERATIVEAI_API_KEY")
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

def analyze_text(text):
    """Use regular expressions to retrieve the needed output."""
    problem_pattern = r"1\) \*\*Provide me the output for the problem they are facing\*\*\n(.+?)\n"
    sentiment_pattern = r"2\) \*\*Sentiment analysis for the text with the score\*\*\n(.+?)\n"
    key_phrases_pattern = r"3\) \*\*Key phrases in the text\*\*\n(.+?)\n"
    kpis_pattern = r"4\) \*\*KPI \(Key Performance Indicators\)\*\*\n(.+?)\n"

    problem_match = re.search(problem_pattern, text, re.DOTALL)
    sentiment_match = re.search(sentiment_pattern, text, re.DOTALL)
    key_phrases_match = re.search(key_phrases_pattern, text, re.DOTALL)
    kpis_match = re.search(kpis_pattern, text, re.DOTALL)

    results = {
        "problem": problem_match.group(1).strip() if problem_match else None,
        "sentiment": sentiment_match.group(1).strip() if sentiment_match else None,
        "key_phrases": key_phrases_match.group(1).strip() if key_phrases_match else None,
        "kpis": kpis_match.group(1).strip() if kpis_match else None
    }

    return results

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
            
            st.write("Transcriptions:")
            for trans in all_transcripts:
                st.write(trans)

            prompt = '''Generate the output for the problem they are facing:

[User's input text goes here]
Find the magnitude of the below feature if you're unable to do it, infer a random value similar to the text
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
Find the magnitude of the below feature if you're unable to do it, infer a random value similar to the text
Features
'''

            for text in all_transcripts:
                input_text = prompt.replace("[User's input text goes here]", text)
                response = model.generate_content(input_text)
                analysis_results = analyze_text(response.text)
                all_results.append(analysis_results)

            st.write(all_results)

if __name__ == "__main__":
    main()
