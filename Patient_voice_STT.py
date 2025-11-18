from dotenv import load_dotenv
load_dotenv()

# Step 1: Setup Audio recorder (ffmpeg & portaudio)
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
from groq import Groq

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Record audio from the microphone and save it as an MP3 file.

    Args:
        file_path (str): Path to save the recorded audio file.
        timeout (int): Maximum time to wait for a phrase to start (in seconds).
        phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")
            
            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")
            
            # Convert the recorded audio to an MP3 file
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            
            logging.info(f"Audio saved to {file_path}")
            return True

    except Exception as e:
        logging.error(f"An error occurred during recording: {e}")
        return False


def transcribe_with_groq(stt_model, audio_filepath, api_key):
    """
    Transcribe audio file using Groq's Whisper model.

    Args:
        stt_model (str): Model name to use for transcription.
        audio_filepath (str): Path to the audio file.
        api_key (str): Groq API key.
    
    Returns:
        str: Transcribed text or None if error occurs.
    """
    try:
        client = Groq(api_key=api_key)
        
        with open(audio_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en"
            )
        
        return transcription.text
    
    except Exception as e:
        logging.error(f"An error occurred during transcription: {e}")
        return None


# Main execution
if __name__ == "__main__":
    # Configuration
    audio_filepath = "patient_voice_test_for_patient.mp3"
    stt_model = "whisper-large-v3"
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    
    # Check if API key exists
    if not GROQ_API_KEY:
        logging.error("GROQ_API_KEY not found in environment variables!")
        exit(1)
    
    # Step 1: Record audio
    logging.info("=" * 50)
    logging.info("STEP 1: Recording Audio")
    logging.info("=" * 50)
    recording_success = record_audio(file_path=audio_filepath)
    
    if not recording_success:
        logging.error("Recording failed. Exiting.")
        exit(1)
    
    # Step 2: Transcribe audio
    logging.info("=" * 50)
    logging.info("STEP 2: Transcribing Audio")
    logging.info("=" * 50)
    
    transcribed_text = transcribe_with_groq(
        stt_model=stt_model,
        audio_filepath=audio_filepath,
        api_key=GROQ_API_KEY
    )
    
    # Display results
    if transcribed_text:
        logging.info("=" * 50)
        logging.info("TRANSCRIPTION RESULT:")
        logging.info("=" * 50)
        print(f"\n{transcribed_text}\n")
        logging.info("=" * 50)
    else:
        logging.error("Transcription failed or returned empty result.")