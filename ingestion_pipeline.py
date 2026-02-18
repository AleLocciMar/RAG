import numpy as np
from zenml import step, pipeline
from pymongo import MongoClient
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

# --- STEP 1: EXTRAÇÃO DO DATA LAKE ---
@step
def ingest_data_from_mongodb() -> list:
    """Extrai documentos brutos do MongoDB."""
    client = MongoClient("mongodb://localhost:27017/")
    db = client["rag_database"]
    collection = db["raw_documents"]
    
    documents = list(collection.find({}, {"_id": 1, "content": 1, "metadata": 1}))
    print(f"📦 Extraídos {len(documents)} documentos do MongoDB.")
    return documents

# --- STEP 2: TRANSFORMAÇÃO (INTEGRIDADE SEMÂNTICA) ---
@step
def split_documents(raw_documents: list) -> list:
    """Aplica o Recursive Character Splitting."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    chunks = []
    for doc in raw_documents:
        texts = splitter.split_text(doc["content"])
        for text in texts:
            chunks.append({
                "text": text,
                "metadata": {
                    "source_id": str(doc["_id"]), # Integridade Referencial
                    **doc.get("metadata", {})
                }
            })
    print(f"✂️ Gerados {len(chunks)} fragmentos (chunks).")
    return chunks

# --- STEP 3: CARGA (VECTOR STORE) ---
@step
def load_to_chroma(chunks: list):
    """Gera embeddings e salva no ChromaDB."""
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection("rag_collection")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk["text"]).tolist()
        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk["text"]],
            metadatas=[chunk["metadata"]]
        )
    print("🚀 Vetores indexados no ChromaDB com sucesso!")

# --- ORQUESTRAÇÃO DO PIPELINE ---
@pipeline
def rag_ingestion_pipeline():
    raw_data = ingest_data_from_mongodb()
    processed_chunks = split_documents(raw_data)
    load_to_chroma(processed_chunks)

if __name__ == "__main__":
    rag_ingestion_pipeline()
