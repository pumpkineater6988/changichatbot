# embedder.py

import json
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# Load scraped and cleaned data
with open("vectors/raw_data.json", "r", encoding="utf-8") as f:
    docs = json.load(f)
print(f"Loaded {len(docs)} documents for embedding.")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Chroma client - stores locally in ./chroma_db
client = chromadb.Client(Settings(
    persist_directory="./chroma_db",
    chroma_db_impl="duckdb+parquet"
))

# Create or get collection
collection_name = "changi_airport_collection"
try:
    collection = client.get_collection(collection_name)
except:
    collection = client.create_collection(name=collection_name)

# Prepare data for upsert
ids = []
documents = []
metadatas = []

for i, doc in enumerate(docs):
    ids.append(f"doc-{i}")
    documents.append(doc["content"])
    metadatas.append({"url": doc.get("url", "")})

# Chroma can auto-embed if you skip `embeddings=` param
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids,
)

client.persist()
print(f"Inserted {len(ids)} documents into Chroma collection '{collection_name}'.")
