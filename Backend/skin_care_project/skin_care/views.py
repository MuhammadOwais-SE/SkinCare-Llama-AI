from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import UserData
from .utils import get_skin_care_suggestions

def skin_care_suggestion(request):
    prompt = request.POST.get('prompt_text', '')
    image = request.FILES.get('image')  # Retrieve the image if provided

    if not prompt:
        return JsonResponse({'error': 'Prompt is required'}, status=400)

    # Validate and save user data with or without an image
    try:
        user_data = UserData.objects.create(
            prompt_text=prompt,
            image=image  # Save image if provided
        )
    except Exception as e:
        return JsonResponse({'error': 'Failed to save user data', 'details': str(e)}, status=500)

    # Generate skin care suggestions
    suggestions = get_skin_care_suggestions(prompt)

    # Return suggestions along with user data info if needed
    return JsonResponse({
        'user_id': user_data.id,
        'suggestions': suggestions
    })
