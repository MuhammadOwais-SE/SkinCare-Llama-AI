import google.generativeai as genai
from django.conf import settings

# Configure the Gemini API key
genai.configure(api_key=settings.GEMINI_API_KEY)
# Add this test function in service.py
def test_import():
    return "Import successful!"

# Try to import it in the shell

# Create the model and configure the generation parameters
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

def fetch_gemini_data(prompt):
    try:
        # Initialize the generative model (Gemini 1.5)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )
        
        
        # Start a chat session
        chat_session = model.start_chat(history=[])
        
        # Send the prompt message to the model and get the response
        response = chat_session.send_message(prompt)
        
        # Return the response text (or handle it based on your needs)
        return response.text

    except Exception as e:
        print(f"Error interacting with Gemini API: {e}")
        return None, str(e)
