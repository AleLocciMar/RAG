import os
import fitz
from pymongo import MongoClient

def seed_scientific_articles(pdf_folder):
    # Converte para caminho absoluto para evitar erro de "no such file"
    abs_pdf_folder = os.path.abspath("rag_base/")
    print(f"📂 Verificando pasta: {abs_pdf_folder}")
    
    client = MongoClient("mongodb://localhost:27017/")
    db = client["rag_database"]
    collection = db["raw_documents"]
    
    if not os.path.exists(abs_pdf_folder):
        print(f"❌ Erro: A pasta {abs_pdf_folder} não existe!")
        return

    for filename in os.listdir(abs_pdf_folder):
        if filename.lower().endswith(".pdf"):
            # A forma mais segura de construir o caminho:
            full_path = os.path.join(abs_pdf_folder, filename)
            
            try:
                with fitz.open(full_path) as doc:
                    text = ""
                    for page in doc:
                        text += page.get_text()
                
                article = {
                    "title": filename,
                    "content": text,
                    "metadata": {"source": "Mendeley", "type": "article"}
                }
                collection.insert_one(article)
                print(f"✅ Sucesso: {filename} atracado no MongoDB.")
            except Exception as e:
                print(f"⚠️ Falha ao processar {filename}: {e}")

if __name__ == "__main__":
    seed_scientific_articles("./artigos")
