import os
import sys
import pandas as pd
import numpy as np

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from core.embeddings import get_embedding_model, get_chroma_collection

def map_category(row):
    queue = str(row.get('queue', '')).lower()
    tags = " ".join([str(row.get(f'tag_{i}', '')) for i in range(1, 9)]).lower()
    
    # 1. Tags take precedence (specific keywords)
    if any(kw in tags for kw in ['security', 'breach', 'password', 'phishing', 'hacked', 'access denied']):
        return "Security"
    if any(kw in tags for kw in ['network', 'vpn', 'wifi', 'dns', 'internet', 'connectivity']):
        return "Network"
    if any(kw in tags for kw in ['database', 'sql', 'query', 'slow', 'oracle', 'mysql']):
        return "Database"
    if any(kw in tags for kw in ['account', 'sso', 'okta', 'login', 'permission', 'iam']):
        return "Access Management"
    if any(kw in tags for kw in ['server', 'k8s', 'infrastructure', 'cloud', 'aws', 'hardware']):
        return "Infrastructure"
    
    # 2. Queue mapping fallback
    if 'it support' in queue: return "Infrastructure"
    if 'technical support' in queue: return "Application"
    if 'service outages' in queue: return "Network"
    if 'billing' in queue: return "Database"
    if 'human resources' in queue: return "Access Management"
    
    return "Application" # Default

def map_priority(p):
    p = str(p).lower()
    if 'low' in p: return "P4 Low"
    if 'medium' in p: return "P3 Medium"
    if 'high' in p: return "P2 High"
    if 'urgent' in p: return "P1 Critical"
    return "P3 Medium"

def ingest_kaggle():
    csv_path = 'data/dataset-tickets-multi-lang-4-20k.csv'
    print(f"🚀 Starting Kaggle DB Ingestion from {csv_path}...")
    
    # Load first 2000 for efficiency
    df = pd.read_csv(csv_path).head(2000)
    
    print(f"📊 Normalizing {len(df)} records...")
    
    df['ticket_id'] = [f"KAG-{i:05d}" for i in range(len(df))]
    df['title'] = df['subject']
    df['description'] = df['body']
    df['resolution'] = df['answer']
    df['category'] = df.apply(map_category, axis=1)
    df['department'] = df['queue']
    df['priority'] = df['priority'].apply(map_priority)
    
    # Fill NAs
    df['resolution'] = df['resolution'].fillna("Investigation in progress.")
    df['description'] = df['description'].fillna("No description provided.")
    df['title'] = df['title'].fillna("No subject")
    
    texts = (df['title'] + " " + df['description']).tolist()
    
    print(f"🧠 Generating embeddings (this may take a minute)...")
    model = get_embedding_model()
    embeddings = model.encode(texts).tolist()
    
    collection = get_chroma_collection()
    
    # Prepare metadata
    metadatas = []
    for _, row in df.iterrows():
        metadatas.append({
            "category": row.category,
            "priority": row.priority,
            "resolution": str(row.resolution)[:1000], # Cap resolution length
            "department": str(row.department)
        })
        
    print(f"💾 Upserting to ChromaDB...")
    collection.upsert(
        ids=df['ticket_id'].tolist(),
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas
    )
    
    print(f"✅ SUCCESSFULLY ingested {len(df)} Kaggle tickets into the intelligence core!")

if __name__ == "__main__":
    ingest_kaggle()
