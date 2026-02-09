from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from config import EMBEDDING_MODEL_NAME

# Point to the project-level vector_store folder
VECTOR_DB_PATH = Path(__file__).resolve().parent.parent / "vector_store/faiss_index"

def load_vector_store():
    """
    Load the FAISS vector store from disk.
    """
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME
    )

    vectorstore = FAISS.load_local(
        str(VECTOR_DB_PATH),
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore