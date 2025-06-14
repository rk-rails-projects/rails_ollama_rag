import chromadb
from sentence_transformers import SentenceTransformer

# Auto CPU fallback
try:
    model = SentenceTransformer("all-MiniLM-L6-v2", device="cuda", cache_folder="./hf_models")
except Exception:
    print("[⚠️] GPU not available. Falling back to CPU.")
    model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

client = chromadb.PersistentClient(path="/home/rahul/projects/rails_ollama_rag/.chroma")
collection = client.get_or_create_collection("rails_codebase")

print(f"[🔎] Total documents in 'rails_codebase':", collection.count())

def query_codebase(prompt, n_results=5):
    embedding = model.encode(prompt)
    results = collection.query(
        query_embeddings=[embedding.tolist()],
        n_results=n_results
    )
    return results["documents"][0] if results["documents"] else []
