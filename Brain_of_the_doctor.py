# Step 1: Setup GROQ API key
from dotenv import load_dotenv
load_dotenv()

import os
import base64
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Step 2: Format image to required format
def encode_image(image_path):
    """
    Encode an image file to base64 format.
    
    Args:
        image_path (str): Path to the image file
    
    Returns:
        str: Base64 encoded image string
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


# Step 3: Setup Multimodal LLM
def analyze_image_with_query(query, base64_image, model="meta-llama/llama-4-scout-17b-16e-instruct"):
    """
    Analyze an image with a text query using Groq's multimodal LLM.
    
    Args:
        query (str): The text query/question about the image
        base64_image (str): Base64 encoded image string
        model (str): Model name to use (default: llama-4-scout-17b-16e-instruct)
    
    Returns:
        str: The AI's response text
    """
    client = Groq(api_key=GROQ_API_KEY)
    
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        }
    ]
    
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model
    )
    
    # Extract and return the response text
    full_response = ""
    for choice in chat_completion.choices:
        if hasattr(choice, "message") and hasattr(choice.message, "content"):
            full_response += choice.message.content
        elif hasattr(choice, "text"):
            full_response += choice.text
    
    return full_response.strip()


# Test code - only runs when script is executed directly
if __name__ == "__main__":
    # Example usage
    image_path = r"D:\MedEcho\MedEcho-AI-Voice-Assistant\acne.jpg"
    query = "Is there something wrong with my face?"
    model = "meta-llama/llama-4-scout-17b-16e-instruct"
    
    print("🔄 Encoding image...")
    encoded_image = encode_image(image_path)
    
    print("🧠 Analyzing image with query...")
    response = analyze_image_with_query(query, encoded_image, model)
    
    print("\n🧠 Model Response:")
    print(response)
    
    # If you want detailed metadata, you can modify the function to return the full object
    # For now, this version returns just the text for easier use in Gradio