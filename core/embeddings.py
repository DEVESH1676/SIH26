import os
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
import sys

# Hack to allow absolute imports from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# Initialize models and DB lazily
_model = None
_client = None
_collection = None

def get_embedding_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(config.EMBEDDING_MODEL_NAME)
    return _model

def get_chroma_collection():
    global _client, _collection
    if _client is None:
        _client = chromadb.PersistentClient(path=config.CHROMA_DB_DIR)
        _collection = _client.get_or_create_collection(
            name=config.COLLECTION_NAME, # Should be updated in config to 'courses'
            metadata={"hnsw:space": "cosine"}
        )
    return _collection

def ingest_courses(csv_path: str):
    """Ingest iGOT training courses from a CSV file into ChromaDB."""
    print(f"Loading course data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Check required columns
    required_cols = ['course_id', 'course_name', 'domain', 'skills_covered', 'description']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
            
    # Combine fields for richer embeddings
    texts = (df['course_name'] + " | " + df['description'] + " | Skills: " + df['skills_covered']).tolist()
    
    print(f"Generating embeddings for {len(texts)} courses... This may take a moment.")
    model = get_embedding_model()
    embeddings = model.encode(texts).tolist()
    
    collection = get_chroma_collection()
    
    print("Inserting course data into ChromaDB...")
    # Prepare metadata list
    metadatas = []
    for _, row in df.iterrows():
        meta = {
            "course_id": str(row.course_id),
            "course_name": str(row.course_name),
            "domain": str(row.domain),
            "skills_covered": str(row.skills_covered)
        }
        metadatas.append(meta)
        
    collection.upsert(
        ids=[str(cid) for cid in df['course_id'].tolist()],
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas
    )
    print("Successfully ingested courses into vector database!")

def embed_document_chunks(text: str, chunk_size: int = 500) -> list:
    """
    Naively chunk a document and return embeddings. 
    Useful for future expansion of the QuizEngine to support huge PDFs.
    """
    words = text.split()
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    
    model = get_embedding_model()
    embeddings = model.encode(chunks).tolist()
    
    return [{"chunk": c, "embedding": e} for c, e in zip(chunks, embeddings)]


if __name__ == "__main__":
    # Test script directly
    csv_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'mock_igot_catalog.csv')
    if os.path.exists(csv_file):
        ingest_courses(csv_file)
    else:
        print(f"No CSV file found at {csv_file}. Please create mock course data first.")
