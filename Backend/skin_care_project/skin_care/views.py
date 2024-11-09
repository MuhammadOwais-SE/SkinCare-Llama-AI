# skin_care/views.py

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import UserData
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import get_skin_care_suggestions  # Make sure this is implemented correctly

@api_view(['POST'])
def skin_care_suggestion(request):
    prompt = request.data.get('prompt_text', '')  # The prompt from the user
    image = request.FILES.get('image')  # Optional image upload from the user

    if not prompt:
        return Response({'error': 'Prompt is required'}, status=400)  # Return error if prompt is missing

    try:
        user_data = UserData.objects.create(
            prompt_text=prompt,  # Save the prompt to your UserData model
            image=image  # Optionally save the image if provided
        )
    except Exception as e:
        return Response({'error': 'Failed to save user data', 'details': str(e)}, status=500)

    # Call to the function that gets the skin care suggestions
    suggestions = get_skin_care_suggestions(prompt)

    # Return the suggestions with the user data ID
    return Response({
        'user_id': user_data.id,
        'suggestions': suggestions
    })

# Simple home view
def home(request):
    return HttpResponse("Welcome to the Skin Care AI App!")
