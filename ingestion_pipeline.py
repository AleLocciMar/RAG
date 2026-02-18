import os
import logging
import re
from typing import List
from pymongo import MongoClient

# --- IMPORTS CORRIGIDOS (PADRÃO 2026) ---
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from zenml import step, pipeline

# --- BYPASS DE SEGURANÇA ---
os.environ["ZENML_DISABLE_LOGGING"] = "true"
os.environ["ZENML_ANALYTICS_OPT_OUT"] = "true"
logging.getLogger().handlers = []

# --- CONFIGURAÇÕES ---
"""
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "rag_database"
COLLECTION_NAME = "artigos"
CHROMA_PATH = "chroma_db" """
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "rag_database"
COLLECTION_NAME = "raw_documents"  # <--- Nome real que o mongosh nos deu
CHROMA_PATH = "chroma_db"

@step
def ingest_data_from_mongodb() -> List[Document]:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    docs = []
    for record in collection.find({}):
        content = record.get("content", "")
        metadata = {"title": record.get("title", "Sem título"), "source": "mongodb"}
        docs.append(Document(page_content=content, metadata=metadata))
    client.close()
    print(f"📦 Extraídos {len(docs)} documentos do MongoDB.")
    return docs

@step
def split_documents(documents: List[Document]) -> List[Document]:
    for doc in documents:
        doc.page_content = doc.page_content.replace("-\n", "").replace("\n", " ")
        doc.page_content = re.sub(r'\s+', ' ', doc.page_content)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    print(f"✂️ Documentos divididos em {len(chunks)} fragmentos.")
    return chunks

@step
def create_embeddings(chunks: List[Document]):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    print(f"✅ Embeddings salvos com sucesso em: {CHROMA_PATH}")

@pipeline
def ingestion_pipeline():
    raw_docs = ingest_data_from_mongodb()
    chunks = split_documents(raw_docs)
    create_embeddings(chunks)

if __name__ == "__main__":
    try:
        print("🚀 Tentando rodar via ZenML...")
        ingestion_pipeline()
    except Exception as e:
        # Se o erro 'body' do Logger.emit ocorrer, o script entra aqui
        print(f"\n⚠️ Erro de Log detectado. Acionando Manual Override...")
        
        # Execução direta ignorando o ZenML
        docs = ingest_data_from_mongodb.__wrapped__() if hasattr(ingest_data_from_mongodb, "__wrapped__") else ingest_data_from_mongodb()
        chunks = split_documents.__wrapped__(docs) if hasattr(split_documents, "__wrapped__") else split_documents(docs)
        create_embeddings.__wrapped__(chunks) if hasattr(create_embeddings, "__wrapped__") else create_embeddings(chunks)
        
        print("\n✨ Processamento concluído com sucesso fora do orquestrador!")
