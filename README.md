#Decoupled RAG Pipeline: ChromaDB + MongoDB + ZenML
This repository features a robust, production-ready implementation of a Retrieval-Augmented Generation (RAG) system. The core architecture focuses on decoupling the vector search layer from the metadata storage, ensuring a scalable and maintainable data lifecycle.

📂 Project Structure
chroma_db/: Persistent directory for the vector database indexing.

docker-compose.yml: Docker configuration to spin up MongoDB and ChromaDB services.

environment.yml: The Conda environment definition for seamless dependency management.

ingestion_pipeline.py: The main script for data processing, embedding generation, and ingestion.

pdf_py_script.py: Specialized script for PDF content extraction and cleaning.

rag_base/: Core logic for query retrieval and LLM generation.

static/: Assets and static files for the application.

🚀 Technical Stack
enML: Enterprise Machine Learning patterns for pipeline orchestration.

ChromaDB: High-performance vector storage and semantic search.

MongoDB: Robust document store for raw text and complex metadata.

Conda: Isolated environment management.

Docker: Containerized infrastructure for database services.

⚙️ Environment Setup
To ensure all dependencies (enML, PyMongo, Chroma, etc.) are correctly installed, use the provided environment.yml file.

1. Create the Conda Environment
Bash
conda env create -f environment.yml
2. Activate the Environment
Bash
conda activate <environment_name_from_yml>
3. Spin up Infrastructure
Ensure you have Docker and Docker Compose installed, then run:

Bash
docker-compose up -d
This will start the MongoDB and ChromaDB containers in the background.

🏗️ The Workflow
PDF Extraction: pdf_py_script.py parses raw PDF documents into clean text.

Ingestion Pipeline: ingestion_pipeline.py converts text into embeddings, stores the vectors in ChromaDB, and maps the full metadata into MongoDB.

Retrieval & Generation: The rag_base module handles incoming queries by performing a semantic search in ChromaDB and enriching the context via MongoDB before sending the prompt to the LLM.

📖 Usage
To process and ingest new documents:

Bash
python ingestion_pipeline.py --input_dir ./Documents/source_pdfs
To run the RAG query interface:

Bash
python -m rag_base.query "Explain the decoupled architecture of this project."
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request or open an issue for architectural improvements.
