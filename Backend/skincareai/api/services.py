import requests
from django.conf import settings

def fetch_gemini_data(prompt, image_file=None):
    try:
        # URL of the Gemini API (replace with the actual endpoint)
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

        # Prepare data for the request
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        # If there's an image file, send it along with the request
        files = {}
        if image_file:
            files = {"image": image_file}

        # Send request to Gemini API with the API key in the query parameters
        response = requests.post(
            url,
            json=data,  # Send the prompt data as JSON
            files=files,  # Attach any image file if provided
            params={"key": settings.GEMINI_API_KEY}  # Include the API key as query parameter
        )

        # Check if the response is successful
        if response.status_code == 200:
            response_data = response.json()
            # Retrieve AI's response from the API
            ai_response = response_data.get("content", [{}])[0].get("parts", [{}])[0].get("text", "No analysis available.")
            return ai_response
        else:
            return f"Error from Gemini API: {response.status_code}"

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "Error calling Gemini API"
