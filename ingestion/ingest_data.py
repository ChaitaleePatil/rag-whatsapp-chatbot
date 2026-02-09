from pathlib import Path
import csv
from collections import defaultdict


from langchain_core.documents import Document
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "enterprise_switch_knowledge_base.csv"
VECTOR_DB_PATH = Path("vector_store/faiss_index")
VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)

def load_and_chunk_csv(csv_path):
    grouped = defaultdict(list)

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["product_series"], row["model"])
            grouped[key].append(row)

    documents = []

    for (series, model), rows in grouped.items():
        lines = []
        for r in rows:
            lines.append(f"{r['feature']}: {r['description']}")

        content = f"""
Product Series: {series}
Model: {model}

Specifications:
""" + "\n".join(lines)

        documents.append(
            Document(
                page_content=content.strip(),
                metadata={
                    "product_series": series,
                    "model": model,
                    "category": rows[0]["category"]
                }
            )
        )

    return documents

# 1. Load + chunk CSV
documents = load_and_chunk_csv(CSV_PATH)

# 2. Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 3. Build FAISS store
vectorstore = FAISS.from_documents(documents, embeddings)
vectorstore.save_local(str(VECTOR_DB_PATH))

print("CSV ingestion complete. Vector store saved.")
