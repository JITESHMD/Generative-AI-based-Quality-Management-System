import os
import streamlit as st
import zipfile
import re
from textblob import TextBlob
from dotenv import load_dotenv
import pandas as pd

from lyzr import VoiceBot
import google.generativeai as genai

load_dotenv()

vb = VoiceBot(api_key="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")
genai.configure(api_key=os.getenv('AIzaSyBxbqUnQvC5tc5YLX_5CVIC-d_vEmHb1Ss'))
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

def calculate_aht(text):
    # Count the number of words in the text
    num_words = len(re.findall(r'\w+', text))

    # Average speaking rate (words per minute)
    speaking_rate = 200

    # Additional time for pauses, responses, and other actions (in minutes)
    additional_time = 1

    # Calculate estimated handling time (in minutes)
    estimated_handling_time = num_words / speaking_rate + additional_time

    return estimated_handling_time

def calculate_fcr(text):
    # Define resolution indicators
    resolution_indicators = ["resolved", "satisfied", "thank you", "problem solved", "issue fixed", "resolved the issue", "solved my problem", "satisfactory resolution"]

    # Count the occurrences of resolution indicators in the text
    num_resolutions = sum(text.lower().count(indicator) for indicator in resolution_indicators)

    # Total number of interactions (assuming each conversation represents an interaction)
    total_interactions = 1  # Assuming one conversation represents one interaction

    # Calculate FCR
    fcr = num_resolutions / total_interactions
    return fcr

def calculate_customer_satisfaction(text):
    # Perform sentiment analysis
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity

    # Assess sentiment score
    if sentiment_score > 0:
        satisfaction = "Positive"
    elif sentiment_score == 0:
        satisfaction = "Neutral"
    else:
        satisfaction = "Negative"

    #return satisfaction, 
    return sentiment_score


def calculate_call_abandonment_rate(text):
    # Split the text into sentences
    sentences = text.split(".")
    
    # Initialize variables
    total_calls = 0
    abandoned_calls = 0

    # Iterate through each sentence to identify abandonment indicators
    for sentence in sentences:
        sentence_lower = sentence.lower().strip()
        if "thank you" in sentence_lower or "goodbye" in sentence_lower or "have a nice day" in sentence_lower:
            total_calls += 1
            if "is there anything else" not in sentence_lower:
                abandoned_calls += 1

    # Calculate abandonment rate
    abandonment_rate = abandoned_calls + total_calls

    return abandonment_rate

def analyze_call_resolution(text):
    """
    This function analyzes the sentiment of a conversation text 
    to provide clues about potential call resolution.

    Args:
        text: String containing the conversation text.

    Returns:
        String: "Likely Resolved" or "Potential Issue" based on sentiment.
    """
    sentiment = TextBlob(text).sentiment
    value=sentiment.polarity
    if sentiment.polarity > 0:  # Positive sentiment
        return value
    elif sentiment.polarity < 0:  # Negative sentiment
        return value
    else:  # Neutral sentiment
        return  value
  
def calculate_transfer_rate(text):
    # Define transfer indicators
    transfer_indicators = [
        "transfer",
        "escalate",
        "forward",
        "redirect",
        "pass on",
        "hand over",
        "send to",
        "route to",
        "refer to",
        "assign to"
    ]

    # Count the occurrences of transfer indicators
    total_transfers = sum(text.lower().count(indicator) for indicator in transfer_indicators)

    # Count the total number of sentences in the conversation
    total_sentences = text.count('.') + 1  # Assuming each sentence ends with a period

    # Calculate transfer rate
    transfer_rate = total_transfers / total_sentences if total_sentences > 0 else 0

    return transfer_rate


def calculate_asa(conversation_text):
    # Split the conversation text into utterances
    utterances = conversation_text.split("\n")

    # Filter out empty utterances
    utterances = [utterance.strip() for utterance in utterances if utterance.strip()]

    # Calculate the total number of words spoken
    total_words = sum(len(utterance.split()) for utterance in utterances)

    # Calculate the total number of utterances
    total_utterances = len(utterances)

    # Calculate the average speed of answer (ASA) in words per utterance
    average_asa = total_words / total_utterances if total_utterances != 0 else 0

    return average_asa


def calculate_call_rating(conversation_text):
    # Define positive keywords indicating positive sentiment
    positive_keywords = ["thank", "good", "super", "great", "help", "okay", "understanding", "confirm", 
                         "satisfaction", "like", "yes", "happy", "excellent", "pleased", "awesome", 
                         "fantastic", "wonderful", "perfect", "impressed", "best", "amazing"]

    # Define negative keywords indicating negative sentiment
    negative_keywords = ["concern", "problem", "penalized", "worry", "suspic", "expire", "refund", 
                         "missing", "cancel", "penalized", "damage", "expired", "angry", "upset", 
                         "disappointed", "unhappy", "unresolved", "unsatisfied", "awful", "horrible", 
                         "terrible", "displeased", "regret", "frustrated", "annoyed"]

    # Initialize call rating
    call_rating = 0

    # Check for positive keywords
    for keyword in positive_keywords:
        if keyword in conversation_text.lower():
            call_rating += 1

    # Check for negative keywords
    for keyword in negative_keywords:
        if keyword in conversation_text.lower():
            call_rating -= 1

    # Ensure the call rating is within bounds [-5, 5]
    call_rating = max(-5, min(5, call_rating))

    return call_rating



def calculate_service_level(conversation_text, time_frame=5):
    """
    Calculate the service level based on the number of responses within a specified time frame.

    Args:
    - conversation_text (str): The conversation text.
    - time_frame (int): Time frame in minutes.

    Returns:
    - service_level (float): Percentage of responses received within the time frame.
    """
    # Count the number of utterances in the conversation text
    utterances = re.findall(r'\b\w+\b', conversation_text)
    total_utterances = len(utterances)

    # Estimate the number of responses received within the time frame
    responses_within_time_frame = sum(1 for utterance in utterances if len(utterance) <= time_frame)

    # Calculate the service level
    service_level = (responses_within_time_frame / total_utterances) * 100

    return service_level

def extract_resolution_time(conversation_text):
    """
    Extract the time to solve the problem from the conversation text.

    Args:
    - conversation_text (str): The conversation text.

    Returns:
    - resolution_time (str): Time taken to solve the problem (in HH:MM:SS format).
    """
    # Define a regular expression pattern to match the time
    time_pattern = r'(\d{1,2}:\d{1,2} (?:AM|PM))\b'

    # Search for the time pattern in the conversation text
    match = re.search(time_pattern, conversation_text, re.IGNORECASE)

    if match:
        # If time found, return it as resolution time
        resolution_time = match.group(1)

        # Calculate time in seconds
        hours, minutes, seconds = map(int, resolution_time.split(':'))
        total_seconds = hours * 3600 + minutes * 60 + seconds

        return total_seconds
    else:
        # If no time found, calculate resolution time based on text length
        # Assume average reading speed of 200 words per minute
        words_per_minute = 200
        words_in_text = len(conversation_text.split())
        time_to_read = words_in_text / words_per_minute  # in minutes
        # Convert time to seconds
        total_seconds = int(time_to_read * 60)
        return total_seconds



def calculate_ces(conversation_text):
    """
    Calculate the Customer Effort Score (CES) based on the conversation text.

    Args:
    - conversation_text (str): The conversation text.

    Returns:
    - ces_score (int): The Customer Effort Score.
    """
    # Define positive and negative keywords indicating ease or difficulty
    positive_keywords = ['easy', 'smooth', 'quick', 'efficient', 'helpful', 'simple', 'convenient', 'seamless', 'prompt']
    negative_keywords = ['difficult', 'frustrating', 'confusing', 'challenging', 'inefficient', 'tedious', 'complicated', 'slow', 'annoying']

    # Convert conversation text to lowercase for case-insensitive matching
    conversation_text = conversation_text.lower()

    # Initialize scores for positive and negative keywords
    positive_score = 0
    negative_score = 0

    # Count occurrences of positive and negative keywords in the conversation text
    for keyword in positive_keywords:
        positive_score += conversation_text.count(keyword)
    for keyword in negative_keywords:
        negative_score += conversation_text.count(keyword)

    # Calculate the net score (positive - negative)
    net_score = positive_score - negative_score

    # Determine CES score based on the net score
    if net_score > 0:
        ces_score = 5  # High ease
    elif net_score == 0:
        ces_score = 3  # Neutral
    else:
        ces_score = 1  # High effort

    return ces_score


def simulate_customer_retention(conversation_text, initial_customers=100):
    """
    This function simulates a customer retention scenario based on 
    hypothetical positive or negative outcomes in a conversation.

    Args:
        conversation_text (str): String containing the conversation text.
        initial_customers (int): Integer representing the starting number of customers (default 100).

    Returns:
        int: The simulated number of retained customers after the conversation.
    """

    # Define thresholds (adjust based on your scenario)
    dissatisfaction_threshold = 0.5  # Higher value indicates higher customer churn
    resolution_threshold = 0.7  # Higher value indicates higher customer retention

    from textblob import TextBlob

    # Analyze overall sentiment of the conversation
    sentiment = TextBlob(conversation_text).sentiment.polarity

    # Calculate customer churn based on sentiment and thresholds
    customer_churn = dissatisfaction_threshold * (1 - sentiment)

    # Calculate customer retention based on resolution and thresholds
    customer_retention = resolution_threshold * sentiment

    # Simulate retained customers after the conversation
    retained_customers = int(initial_customers * (1 - customer_churn) * customer_retention)

    return retained_customers


def calculate_compliance_adherence_rate(conversation_text):
    """
    Calculate the compliance adherence rate based on the presence of compliance keywords 
    in the conversation text.

    Args:
        conversation_text (str): String containing the conversation text.

    Returns:
        float: Compliance adherence rate (percentage).
    """
    compliance_keywords = ["follow script", "adhere to policy", "regulatory compliance", "standard procedure"]
    total_keywords = len(compliance_keywords)
    noncompliance_count = 0

    # Check if any compliance keywords are present in the conversation text
    for keyword in compliance_keywords:
        if keyword.lower() in conversation_text.lower():
            noncompliance_count += 1

    # Calculate compliance adherence rate
    if total_keywords > 0:
        compliance_adherence_rate = ((total_keywords - noncompliance_count) / total_keywords) * 100
    else:
        compliance_adherence_rate = 100  # Default to 100% if no compliance keywords provided

    return int(compliance_adherence_rate)

def main():
    st.title("Generative AI-based QMS ")
    files = upload()
    bname = st.button("PROCESS")
    extract = r"C:\Users\amjat\Desktop\airlines voice\extracted"
    
    if bname:
        if files:
            extract_zip(files.name, extract)
            all_transcripts = []
            handling_time=[]
            call_resolve=[]
            statisfaction=[]
            abodant_rate=[]
            call_resolution=[]
            transfer_rate = []
            average_sa=[]
            call_rating=[]
            ###########################################################
            service_level = []
            resolution_time=[]
            cal_ces=[]
            customer_retention=[]
            compliance_adherence_rate=[]
            
            for file in os.listdir(extract):
                audio_file_path = os.path.join(extract, file)
                trans = transcribe(audio_file_path)
                all_transcripts.extend(trans)
            
            for trans in all_transcripts:
                ahd=calculate_aht(trans)
                handling_time.append(ahd)

                call=calculate_fcr(trans)
                call_resolve.append(call)

                statisfy=calculate_customer_satisfaction(trans)
                statisfaction.append(statisfy)

                abodant=calculate_call_abandonment_rate(trans)
                abodant_rate.append(abodant)

                care=analyze_call_resolution(trans)
                call_resolution.append(care)

                rate=calculate_transfer_rate(trans)
                transfer_rate.append(rate)

                ase=calculate_asa(trans)
                average_sa.append(ase)

                rating=calculate_call_rating(trans)
                call_rating.append(rating)

                cal=calculate_service_level(trans,5)
                service_level.append(cal)

                time=extract_resolution_time(trans)
                resolution_time.append(time)

                ces=calculate_ces(trans)
                cal_ces.append(ces)

                cus=simulate_customer_retention(trans,100)
                customer_retention.append(cus)

                cc=calculate_compliance_adherence_rate(trans)
                compliance_adherence_rate.append(cc)

            # Create a dataframe to store the results
            df = pd.DataFrame({
                'Handling Time': handling_time,
                'First Call Resolution': call_resolve,
                'Customer Satisfaction': statisfaction,
                'Abandonment Rate': abodant_rate,
                'Call Resolution': call_resolution,
                'Transfer Rate': transfer_rate,
                'Average Speed of Answer (ASA)': average_sa,
                'Call Rating': call_rating,
                'Service Level': service_level,
                'Resolution Time': resolution_time,
                'Customer Effort Score (CES)': cal_ces,
                'Customer Retention': customer_retention,
                'Compliance Adherence Rate': compliance_adherence_rate
            })

            # Display the dataframe
            st.dataframe(df)

            # Plot each list
            st.line_chart(df)

            # Plot each feature in the column
            for column in df.columns:
                if column != 'Customer Satisfaction':  # Exclude 'Customer Satisfaction' for plotting as it's not numerical
                    if st.checkbox(f"Plot {column} as line chart"):
                        st.line_chart(df[column])
                    if st.checkbox(f"Plot {column} as bar chart"):
                        st.bar_chart(df[column])

if __name__ == "__main__":
    main()
