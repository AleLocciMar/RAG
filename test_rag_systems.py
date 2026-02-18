import os
from pymongo import MongoClient
import chromadb
from sentence_transformers import SentenceTransformer

def test_systems():
    print("🚀 Iniciando Diagnóstico de Sistemas...")

    # 1. Teste MongoDB (Data Lake)
    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        client.server_info()
        print("✅ [MongoDB] Conectado com sucesso ao Data Lake.")
    except Exception as e:
        print(f"❌ [MongoDB] Falha: Verifique se o Docker está rodando. Erro: {e}")

    # 2. Teste ChromaDB (Vector Store)
    try:
        chroma_client = chromadb.PersistentClient(path="./test_chroma")
        collection = chroma_client.get_or_create_collection(name="test_collection")
        collection.add(documents=["Teste de sanidade"], ids=["id1"])
        print("✅ [ChromaDB] Vector Store operacional (Local Persistence).")
    except Exception as e:
        print(f"❌ [ChromaDB] Falha: {e}")

    # 3. Teste Sentence-Transformers (Embeddings)
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        vector = model.encode("A NCC-1701-D está pronta.")
        print(f"✅ [Embeddings] Modelo carregado. Vetor gerado (Dimensões: {len(vector)})")
    except Exception as e:
        print(f"❌ [Embeddings] Falha ao carregar modelo: {e}")

if __name__ == "__main__":
    test_systems()
