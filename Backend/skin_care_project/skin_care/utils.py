import requests

def get_skin_care_suggestions(prompt: str):
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyBWPFrTW4kRQK8Fel6fW5A_BOK4QTfo01w'  # Gemini API URL
    headers = {
        'Authorization': 'Bearer YOUR_API_KEY',  # Make sure to replace this with a valid API key
        'Content-Type': 'application/json'  # Ensure correct content type
    }
    data = {
        'prompt': prompt,
        'parameters': {
            'skin_type': 'dry',  # Customize this if needed based on Gemini's API
            'other_params': 'value'  # Modify as per Gemini API docs
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        # Check if the request was successful
        response.raise_for_status()  # Will raise an exception for HTTP error responses
        
        return response.json()  # Return the parsed JSON response from the API
    
    except requests.exceptions.RequestException as e:
        # Handle errors like connection issues, timeouts, etc.
        return {'error': str(e)}

    except Exception as e:
        # Handle any other unexpected errors
        return {'error': f"An unexpected error occurred: {str(e)}"}
