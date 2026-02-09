import uvicorn
from fastapi import FastAPI
from whatsapp import webhook
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()
@app.get("/")
def health_check():
    return {"status": "server running"}

# Create FastAPI instance
app = FastAPI(title="RAG WhatsApp Chatbot")

# Include WhatsApp webhook routes
app.include_router(webhook.app.router)

if __name__ == "__main__":
    # Run the FastAPI server on port 8000
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
