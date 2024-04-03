import streamlit as st
from lyzr import VoiceBot
import os
import zipfile
from dotenv import load_dotenv
from google.generativeai.models import GenerativeModel
from google.generativeai import genai
import matplotlib.pyplot as plt

load_dotenv()
all_results = []

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

def calculate_abandonment_rate(conversation):
    num_abandoned_calls = conversation.lower().count("disconnected") + conversation.lower().count("hung up")
    total_calls = 1
    abandonment_rate = num_abandoned_calls / total_calls
    return abandonment_rate

def calculate_resolution_rate(conversation):
    resolution_indicators = ["resolved", "satisfied", "thank you", "problem solved"]
    issue_resolved = any(indicator in conversation.lower() for indicator in resolution_indicators)
    resolution_rate = 1 if issue_resolved else 0
    return resolution_rate

def calculate_transfer_rate(conversation):
    transfer_keywords = ["transferred", "transfer the call", "transferring you"]
    num_transfers = 0
    segments = conversation.split(".")
    for segment in segments:
        if any(keyword in segment.lower() for keyword in transfer_keywords):
            num_transfers += 1
    total_calls = 1
    transfer_rate = num_transfers / total_calls
    return transfer_rate

def calculate_asa(conversation):
    asa = 2.5  # Placeholder value
    return asa

def calculate_error_rate(conversation):
    error_keywords = ["error", "issue", "problem", "mistake", "incorrect", "fault", "apology", "sorry"]
    num_errors = sum(conversation.lower().count(keyword) for keyword in error_keywords)
    total_words = len(conversation.split())
    error_rate = (num_errors / total_words) * 100
    return error_rate

def plot_kpi_magnitudes(magnitudes):
    functions = ['AHT', 'FCR', 'CSAT', 'Abandonment Rate', 'Transfer Rate', 'ASA', 'Call Rating', 'Silence Ratio', 'Overcall Rate', 'Error Rate']
    plt.figure(figsize=(10, 6))
    plt.barh(functions, magnitudes, color='skyblue')
    plt.xlabel('Magnitude')
    plt.title('Key Performance Indicators (KPIs)')
    st.pyplot()

def main():
    uploaded_file = upload()
    if uploaded_file:
        # Extract uploaded zip file
        extract_zip(uploaded_file.name, "temp_folder")
        
        # Transcribe audio files in the extracted folder
        for file_name in os.listdir("temp_folder"):
            if file_name.endswith('.wav'):  # Assuming audio files are in wav format
                file_path = os.path.join("temp_folder", file_name)
                conversation_text = transcribe(file_path)
                
                # Calculate KPI magnitudes
                aht_magnitude = 5  # Placeholder value
                fcr_magnitude = calculate_resolution_rate(conversation_text)
                csat_magnitude = 3  # Placeholder value
                abandonment_rate = calculate_abandonment_rate(conversation_text)
                transfer_rate = calculate_transfer_rate(conversation_text)
                asa = calculate_asa(conversation_text)
                call_rating_magnitude = 4  # Placeholder value
                silence_ratio_magnitude = 2  # Placeholder value
                overcall_rate_magnitude = 1  # Placeholder value
                error_rate_magnitude = calculate_error_rate(conversation_text)
                
                # Plot KPI magnitudes
                magnitudes = [aht_magnitude, fcr_magnitude, csat_magnitude, abandonment_rate, transfer_rate, asa, call_rating_magnitude, silence_ratio_magnitude, overcall_rate_magnitude, error_rate_magnitude]
                plot_kpi_magnitudes(magnitudes)
                break  # Only process the first audio file for demonstration

if __name__ == "__main__":
    main()
