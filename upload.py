import streamlit as st
from lyzr import VoiceBot  # Assuming you have VoiceBot installed
import os
import zipfile
from google.generativeai import genai  # Assuming you have the GenerativeAI library
load_dotenv()
# Load environment variables (if using)
vb = VoiceBot(api_key="")
genai.configure(api_key="AIzaSyBxbqUnQvC5tc5YLX_5CVIC-d_vEmHb1Ss")
model = genai.GenerativeModel('gemini-pro')
def upload_and_extract_audio():
    """Uploads a zip file, extracts audio if present, and returns the audio file path."""
    uploaded_file = st.file_uploader("Upload a Zip File (containing audio)", type=["zip"])
    if uploaded_file is not None:
        try:
            with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    if file_info.filename.endswith('.mp3'):
                        file_info.filename = os.path.basename(file_info.filename)
                        extract_path = os.path.join(os.getcwd(), "extracted")
                        os.makedirs(extract_path, exist_ok=True)  # Create extraction directory if needed
                        zip_ref.extract(file_info, extract_path)
                        return os.path.join(extract_path, file_info.filename)
        except Exception as e:
            st.error(f"Error extracting audio: {str(e)}")
    return None

def transcribe_audio(audio_file_path):
    """Transcribes the audio file using VoiceBot and returns the transcript."""
    if audio_file_path:
        try:
            transcript = vb.transcribe(audio_file_path)
            return transcript.text
        except Exception as e:
            st.error(f"Error transcribing audio: {str(e)}")
    return None

def analyze_text(text):
    """Analyzes the text using GenerativeAI to extract problem, sentiment, key phrases, and KPIs."""

    prompt = f'''Generate the output for the problem they are facing:

{text}
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
'''

    response = model.generate_content(prompt)

    if not response or not hasattr(response, 'text'):
        return None

    content = response.text
    parts = content.split("**")

    results = {
        "problem": parts[1].strip(),
        "sentiment": parts[3].strip(),
        "key_phrases": [phrase.strip() for phrase in parts[5].strip().splitlines()],
        "kpis": {}
    }

    if len(parts) > 7:
        try:
            kpi_data = json.loads(parts[7])
            results["kpis"] = kpi_data
        except json.JSONDecodeError:
            st.error("Error parsing KPI data from response")

    return results

def main():
    st.title("Customer Call Quality Analysis")

    audio_file_path = upload_and_extract_audio()

    if audio_file_path:
        transcript = transcribe_audio(audio_file_path)

        if transcript:
            analysis_results = analyze_text(transcript)

            if analysis_results:
                st.subheader("Analysis Results:")

                st.write("**Problem Identified:**")
