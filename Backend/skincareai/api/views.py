from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from .services import fetch_gemini_data
from .models import Conversation, Message
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def create_message(request):
    try:
        # Extract data from the request
        prompt_text = request.data.get('message', '')  # The message text
        image_file = request.FILES.get('image')  # Optional image from the user
        conversation_id = request.data.get('conversation_id')  # ID of the current conversation

        logger.info(f"Received request - Text: {prompt_text}, Image: {bool(image_file)}, Conversation: {conversation_id}")

        # Validate input: either message or image is required
        if not prompt_text and not image_file:
            return Response({
                "message": "Either message text or image is required",
                "status": "error"
            }, status=400)

        # Convert conversation_id to UUID (if not already)
        try:
            conversation_id = UUID(conversation_id)  # Convert to UUID if it's a valid UUID string
            logger.info(f"Converted conversation_id: {conversation_id}")
        except ValueError:
            logger.error(f"Invalid conversation_id format: {conversation_id}")
            return Response({
                "message": "Invalid conversation_id format",
                "status": "error"
            }, status=400)

        # Get the conversation object
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            logger.info(f"Found conversation: {conversation}")
        except Conversation.DoesNotExist:
            logger.error(f"Conversation with ID {conversation_id} not found.")
            return Response({
                "message": "Conversation not found",
                "status": "error"
            }, status=404)

        # Create a user message in the database
        user_message = Message.objects.create(
            conversation=conversation,
            user=None,  # Can be None if authentication is not used
            message_text=prompt_text,
            is_ai_response=False,
            image=image_file
        )

        logger.info(f"Created user message with ID: {user_message.id}")

        # Construct the prompt for AI based on the input
        context_prompt = (
            "You are a skincare AI assistant. "
            f"Provide helpful advice for the following question: {prompt_text}"
        )

        # Fetch AI response using Gemini
        ai_response = fetch_gemini_data(context_prompt, image_file)

        if ai_response:
            # Save AI response to the database
            ai_message = Message.objects.create(
                conversation=conversation,
                user=None,  # Can be None if authentication is not used
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
            "detail": str(e)
        }, status=500)
