from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from django.shortcuts import get_object_or_404
from .services import fetch_gemini_data
from .models import Message, Conversation
import logging

# Set up logging
logger = logging.getLogger(__name__)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def create_message(request):
    try:
        # Extract data from request
        prompt_text = request.data.get('message', '')  # Changed from 'prompt_text' to match frontend
        image_file = request.FILES.get('image')
        conversation_id = request.data.get('conversation_id')
        
        logger.info(f"Received request - Text: {prompt_text}, Image: {bool(image_file)}, Conversation: {conversation_id}")
        
        # Validate input
        if not prompt_text and not image_file:
            return Response({
                "message": "Either message text or image is required",
                "status": "error"
            }, status=400)
            
        # Get or create conversation
        try:
            conversation = Conversation.objects.get(id=conversation_id)  # Changed from conversation_id to id
        except Conversation.DoesNotExist:
            conversation = Conversation.objects.create(id=conversation_id)
        
        # Create user message
        user_message = Message.objects.create(
            conversation=conversation,
            user=request.user if request.user.is_authenticated else None,  # Handle anonymous users
            message_text=prompt_text,
            is_ai_response=False,
            image=image_file
        )
        
        logger.info(f"Created user message with ID: {user_message.id}")

        # Construct prompt based on context
        if image_file:
            context_prompt = (
                "You are a skincare AI assistant. Analyze the uploaded skin image and provide detailed "
                "observations about skin conditions, potential concerns, and recommendations. "
                f"User's question: {prompt_text}"
            )
        else:
            context_prompt = (
                "You are a skincare AI assistant. Provide helpful advice and recommendations "
                f"for the following question: {prompt_text}"
            )

        # Get AI response
        ai_response = fetch_gemini_data(context_prompt, image_file)
        
        logger.info("Received AI response")

        if ai_response:
            # Save AI response
            ai_message = Message.objects.create(
                conversation=conversation,
                user=request.user if request.user.is_authenticated else None,
                message_text=ai_response,
                is_ai_response=True
            )
            
            logger.info(f"Created AI message with ID: {ai_message.id}")
            
            return Response({
                "message": ai_response,
                "status": "success",
                "message_id": ai_message.id
            })
        else:
            logger.error("Empty AI response received")
            return Response({
                "message": "Failed to get AI response",
                "status": "error"
            }, status=400)
            
    except Exception as e:
        logger.error(f"Error in create_message: {str(e)}", exc_info=True)
        return Response({
            "message": "An error occurred processing your request",
            "status": "error",
            "detail": str(e) if settings.DEBUG else "Internal server error"
        }, status=500)