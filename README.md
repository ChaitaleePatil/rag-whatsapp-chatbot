# RAG-Based WhatsApp AI Chatbot

**Project:** Change Networks Assistant  
**Objective:** Build an AI-powered WhatsApp chatbot using Retrieval-Augmented Generation (RAG) that can answer queries from a domain-specific dataset and remember past conversations.

---

## Features

- Uses **RAG (Retrieval-Augmented Generation)** for accurate responses from your dataset.
- **Context retention**: remembers previous conversations per user.
- Fully functional **WhatsApp bot** via Twilio integration.
- Formatted responses for **readable WhatsApp messages**.
- Supports multi-user sessions.

---

## Project Structure

rag-whatsapp-chatbot/
│
├─ whatsapp/ # WhatsApp integration
│ ├─ webhook.py # Handles incoming messages
│ ├─ context_db.py # Stores and retrieves conversation history
│ └─ chat_memory.db # SQLite database for session storage
│
├─ rag/ # RAG pipeline
│ ├─ rag_chain.py # Build & run RAG chain
│ └─ vector_store.py # Load and manage vector embeddings
│
├─ vector_store/faiss_index/ # Prebuilt FAISS vector store
├─ utils/formatter.py # Format WhatsApp responses
├─ memory/session_manager.py # Optional session management
├─ requirements.txt # Python dependencies
└─ app.py # FastAPI app entrypoint



## Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/ChaitaleePatil/rag-whatsapp-chatbot.git
cd rag-whatsapp-chatbot
Create virtual environment


python -m venv venv
source venv/Scripts/activate   # Windows

pip install -r requirements.txt
Configure environment variables
Create a .env file with your Twilio credentials:


TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
Run the FastAPI app


python app.py
Expose endpoint (for testing WhatsApp)
Use ngrok or any public tunneling service:


ngrok http 8000
Copy the public URL to Twilio webhook.

Usage
Open WhatsApp and send a message to your bot number.

The bot will reply: "Processing your query, reply will come soon!"

The RAG chain will generate the answer using the dataset and context.

Responses are stored in the database for conversation history.


Demo Video
See the demo video showing live WhatsApp interactions, multi-user support, and database logging.
