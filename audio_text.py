import os
import assemblyai as aai

# Replace with your API key
aai.settings.api_key = "4e36f069d21d46c481552d56b7bbbf87"

# Directory containing audio files
CALL_DATA_DIR = "Call Data Sample"

# Create a directory to store transcript files if it doesn't exist
if not os.path.exists("Transcripts"):
    os.makedirs("Transcripts")

# Iterate over each audio file in the directory
for filename in os.listdir(CALL_DATA_DIR):
    if filename.endswith(".mp3"):
        # Path to the audio file
        file_path = os.path.join(CALL_DATA_DIR, filename)
        
        # Transcribe the audio file
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(file_path)
        
        if transcript.status == aai.TranscriptStatus.error:
            print(f"Error transcribing {filename}: {transcript.error}")
        else:
            # Write transcript to a text file
            transcript_text = transcript.text
            transcript_filename = os.path.splitext(filename)[0] + ".txt"
            transcript_filepath = os.path.join("Transcripts", transcript_filename)
            with open(transcript_filepath, "w") as f:
                f.write(transcript_text)
            print(f"Transcript saved for {filename}")
