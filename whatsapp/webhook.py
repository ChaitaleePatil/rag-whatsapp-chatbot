from fastapi import FastAPI, Form
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import asyncio
from concurrent.futures import ThreadPoolExecutor
import traceback
from rag.rag_chain import get_rag_chain
from utils.formatter import format_whatsapp_response, add_intro
import os
from .context_db import add_message, get_history

app = FastAPI()

# Twilio client for sending follow-up messages
TWILIO_CLIENT = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"

# Global thread executor for blocking RAG calls
executor = ThreadPoolExecutor()

# Load RAG chain once
RAG_CHAIN = get_rag_chain(user_id="default")

@app.post("/whatsapp")
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(...)
):
    user_number = From
    user_message = Body

    # Save user message
    add_message(user_number, "user", user_message)

    # Respond immediately
    resp = MessagingResponse()
    resp.message("⏳ Processing your query, reply will come soon!")

    # Process RAG in background
    asyncio.create_task(process_rag_response(user_number, user_message))

    return str(resp)



async def process_rag_response(user_number: str, user_message: str):
    """Runs RAG and sends the result via Twilio API, including chat history."""
    try:
        # Load previous history for context
        history = get_history(user_number)

        # Build a context prompt
        context_text = ""
        for msg in history[-10:]:  # include last 10 messages
            speaker = "User" if msg["role"] == "user" else "Assistant"
            context_text += f"{speaker}: {msg['content']}\n"

        # Add current question
        context_text += f"User: {user_message}\nAssistant:"

        # Run RAG with context
        result = await asyncio.get_event_loop().run_in_executor(
            executor,
            lambda: RAG_CHAIN.invoke(context_text)
        )

        # Save assistant's response
        add_message(user_number, "assistant", result)

        # Format and send response
        formatted_result = add_intro(format_whatsapp_response(result))
        TWILIO_CLIENT.messages.create(
            body=formatted_result,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=user_number
        )

    except Exception as e:
        traceback.print_exc()
        # Send error message
        try:
            TWILIO_CLIENT.messages.create(
                body="⚠️ Sorry, I'm busy or my service quota is full. Please try again later!",
                from_=TWILIO_WHATSAPP_NUMBER,
                to=user_number
            )
        except Exception as e2:
            traceback.print_exc()
