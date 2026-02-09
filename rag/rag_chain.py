import os
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

from rag.vector_store import load_vector_store
from memory.session_manager import get_user_memory
from config import GEMINI_MODEL_NAME, LLM_TEMPERATURE

# Load environment variables from .env
load_dotenv()


def get_rag_chain(user_id: str):
    """
    Create or fetch a Conversational RAG chain for a given user.
    """

    # Load vector store
    vectorstore = load_vector_store()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    # Load conversation memory for this user
    memory = get_user_memory(user_id)

    # Initialize Gemini LLM with Google API key
    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL_NAME,
        temperature=LLM_TEMPERATURE,
        api_key=os.getenv("GOOGLE_API_KEY")  # explicitly use GOOGLE_API_KEY
    )

    # Prompt template (valid roles only: system, human, ai/assistant)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use the following context to answer the user’s question:\n{context}"),
        ("human", "{question}")
    ])

    # Build RAG chain manually
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain