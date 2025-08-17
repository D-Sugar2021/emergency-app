import time

def transcribe(file_path: str) -> str:
    """
    Simulates a long-running transcription process.
    """
    print(f"Starting dummy transcription for {file_path}...")
    time.sleep(5)  # Simulate a 5-second processing time
    print("Dummy transcription complete.")
    return "This is a dummy transcription of the audio file."

def summarize(text: str) -> str:
    """
    Simulates summarizing a text.
    """
    print("Starting dummy summarization...")
    time.sleep(2)  # Simulate a 2-second processing time
    summary = "This is a dummy summary."
    print("Dummy summarization complete.")
    return summary
