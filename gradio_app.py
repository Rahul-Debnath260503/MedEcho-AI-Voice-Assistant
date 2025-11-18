import os
import gradio as gr
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import your custom functions
from Brain_of_the_doctor import encode_image, analyze_image_with_query
from Patient_voice_STT import transcribe_with_groq 
from Doctor_voice_TTS import text_to_speech_with_gtts

# Configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
STT_MODEL = "whisper-large-v3"

def process_inputs(audio_file, image_file):
    """
    Process voice input and image, return transcription, AI analysis, and audio response.
    """
    try:
        # Initialize outputs
        transcribed_text = ""
        ai_response = ""
        audio_output = None
        
        # Step 1: Transcribe audio if provided
        if audio_file is not None:
            try:
                transcribed_text = transcribe_with_groq(
                    stt_model=STT_MODEL,
                    audio_filepath=audio_file,
                    api_key=GROQ_API_KEY  # Changed parameter name
                )
            except Exception as e:
                transcribed_text = f"Audio transcription failed: {str(e)}"
        else:
            transcribed_text = "No audio provided"
        
        # Step 2: Analyze image if provided
        if image_file is not None and transcribed_text and "failed" not in transcribed_text.lower():
            try:
                base64_image = encode_image(image_file)
                ai_response = analyze_image_with_query(
                    query=transcribed_text,
                    base64_image=base64_image
                )
            except Exception as e:
                ai_response = f"Image analysis failed: {str(e)}"
        else:
            ai_response = "No image provided or invalid query"
        
        # Step 3: Convert response to speech
        if ai_response and "failed" not in ai_response.lower():
            try:
                audio_output = "temp_response.mp3"
                text_to_speech_with_gtts(ai_response, audio_output)
            except Exception as e:
                print(f"TTS failed: {str(e)}")
                audio_output = None
        
        return transcribed_text, ai_response, audio_output
    
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        return error_msg, error_msg, None

# Create Gradio interface with explicit component definitions
with gr.Blocks(title="MedEcho AI Doctor") as demo:
    gr.Markdown("# 🩺 MedEcho AI Doctor Voice Assistant")
    gr.Markdown("Upload a medical image and speak your question to get an AI analysis with voice response.")
    
    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="🎤 Record Your Question"
            )
            image_input = gr.Image(
                type="filepath",
                label="📸 Upload Medical Image"
            )
            submit_btn = gr.Button("🔍 Analyze", variant="primary")
        
        with gr.Column():
            text_output = gr.Textbox(
                label="📝 Your Question (Transcribed)",
                lines=3
            )
            response_output = gr.Textbox(
                label="🤖 AI Doctor Response",
                lines=10
            )
            audio_output = gr.Audio(
                label="🔊 Voice Response",
                type="filepath"
            )
    
    # Connect the button to the function
    submit_btn.click(
        fn=process_inputs,
        inputs=[audio_input, image_input],
        outputs=[text_output, response_output, audio_output]
    )

# Launch the app
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting MedEcho AI Doctor Assistant...")
    print("=" * 60)
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        debug=True,
        share=False,
        inbrowser=True  # This will automatically open your browser
    )