import requests

def get_skin_care_suggestions(prompt: str):
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyBWPFrTW4kRQK8Fel6fW5A_BOK4QTfo01w'  # Replace with Gemini/Llama API endpoint
    headers = {'Authorization': 'Bearer YOUR_API_KEY'}
    data = {
        'prompt': prompt,
        'parameters': {'skin_type': 'dry', 'other_params': 'value'}  # Adjust based on Gemini's API
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()  # Assuming the response is in JSON format
