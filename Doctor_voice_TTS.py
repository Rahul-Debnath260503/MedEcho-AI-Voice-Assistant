# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()

# Step1a: Setup Text to Speech–TTS–model with gTTS
import os
from gtts import gTTS

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)


# Step1b: Setup Text to Speech–TTS–model with ElevenLabs
import elevenlabs
from elevenlabs.client import ElevenLabs

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")  # Fixed: matches .env variable name

def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)


# Step2: Use Model for Text output to Voice with Autoplay

import subprocess
import platform

def text_to_speech_with_gtts(input_text, output_filepath):
    """
    Generate speech from text using gTTS and save (no autoplay for Gradio).
    
    Args:
        input_text (str): Text to convert to speech
        output_filepath (str): Path to save the MP3 file
    """
    language = "en"
    
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    print(f"✅ Audio saved to: {output_filepath}")
    
    # Note: Autoplay removed for Gradio compatibility
    # Gradio will handle playback in the browser


def text_to_speech_with_gtts_autoplay(input_text, output_filepath):
    """
    Generate speech with autoplay (for standalone use, not Gradio).
    Uses Windows-compatible playback method.
    """
    language = "en"
    
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            # Use windows media player for MP3 support
            os.startfile(output_filepath)
        elif os_name == "Linux":  # Linux
            subprocess.run(['mpg123', output_filepath])  # or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


def text_to_speech_with_elevenlabs(input_text, output_filepath):
    """
    Generate speech from text using ElevenLabs and save (no autoplay for Gradio).
    
    Args:
        input_text (str): Text to convert to speech
        output_filepath (str): Path to save the MP3 file
    """
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)
    print(f"✅ Audio saved to: {output_filepath}")
    
    # Note: Autoplay removed for Gradio compatibility
    # Gradio will handle playback in the browser


def text_to_speech_with_elevenlabs_autoplay(input_text, output_filepath):
    """
    Generate speech with autoplay using ElevenLabs (for standalone use, not Gradio).
    """
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)
    
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            os.startfile(output_filepath)
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


# Test code
if __name__ == "__main__":
    input_text = "Hi this is AI Doctor, testing!"
    
    # Test basic gTTS (no autoplay)
    print("Testing gTTS (no autoplay)...")
    text_to_speech_with_gtts(input_text, "gtts_test.mp3")
    
    # Uncomment to test with autoplay
    # print("Testing gTTS with autoplay...")
    # text_to_speech_with_gtts_autoplay(input_text, "gtts_autoplay_test.mp3")
    
    # Uncomment to test ElevenLabs
    # print("Testing ElevenLabs (no autoplay)...")
    # text_to_speech_with_elevenlabs(input_text, "elevenlabs_test.mp3")